"""LinkedIn automation module for connecting and messaging."""

import time
import logging
from typing import Dict, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import config

logger = logging.getLogger(__name__)


class LinkedInAutomationError(Exception):
    """Custom exception for LinkedIn automation errors."""
    pass


class LinkedInConnector:
    """Handles LinkedIn authentication and connection requests."""
    
    def __init__(self, email: str = None, password: str = None):
        """
        Initialize LinkedIn connector.
        
        Args:
            email: LinkedIn email (defaults to config)
            password: LinkedIn password (defaults to config)
        """
        self.email = email or config.LINKEDIN_EMAIL
        self.password = password or config.LINKEDIN_PASSWORD
        self.driver = None
        self.is_logged_in = False
        
        if not self.email or not self.password:
            raise LinkedInAutomationError(
                "LinkedIn credentials not provided. Set LINKEDIN_EMAIL and "
                "LINKEDIN_PASSWORD in .env file or pass them as arguments."
            )
    
    def _init_driver(self):
        """Initialize Chrome WebDriver."""
        chrome_options = Options()
        
        if config.HEADLESS_MODE:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        logger.info("Chrome WebDriver initialized")
    
    def login(self) -> bool:
        """
        Login to LinkedIn.
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            if not self.driver:
                self._init_driver()
            
            logger.info("Navigating to LinkedIn login page")
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                self.is_logged_in = True
                logger.info("Successfully logged in to LinkedIn")
                return True
            else:
                logger.error("Login failed - unexpected redirect")
                return False
                
        except TimeoutException:
            logger.error("Login timeout - page elements not found")
            return False
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False
    
    def search_people(self, company: str, role: str) -> bool:
        """
        Search for people by company and role.
        
        Args:
            company: Company name
            role: Target role/title
            
        Returns:
            True if search successful
        """
        try:
            search_query = f"{role} {company}"
            search_url = (
                f"https://www.linkedin.com/search/results/people/?"
                f"keywords={search_query.replace(' ', '%20')}"
            )
            
            logger.info(f"Searching for: {search_query}")
            self.driver.get(search_url)
            time.sleep(3)
            
            return True
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return False
    
    def send_connection_request(
        self, 
        target_data: Dict[str, str],
        message_template: str = None
    ) -> Dict[str, Any]:
        """
        Send connection request with personalized message.
        
        Args:
            target_data: Dictionary with company, sector, target_role
            message_template: Custom message template (uses default if None)
            
        Returns:
            Dictionary with status and details
        """
        result = {
            'success': False,
            'company': target_data['company'],
            'role': target_data['target_role'],
            'message': ''
        }
        
        try:
            if not self.is_logged_in:
                result['message'] = "Not logged in to LinkedIn"
                return result
            
            # Search for people
            if not self.search_people(target_data['company'], target_data['target_role']):
                result['message'] = "Search failed"
                return result
            
            # Find connect buttons on the page
            connect_buttons = self.driver.find_elements(
                By.XPATH, 
                "//button[contains(@aria-label, 'Invite') or contains(text(), 'Connect')]"
            )
            
            if not connect_buttons:
                result['message'] = "No connection buttons found"
                logger.warning(f"No people found for {target_data['company']} - {target_data['target_role']}")
                return result
            
            # Click the first available connect button
            connect_buttons[0].click()
            time.sleep(2)
            
            # Try to add a note if the option is available
            try:
                add_note_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Add a note')]"))
                )
                add_note_button.click()
                time.sleep(1)
                
                # Prepare message
                template = message_template or config.DEFAULT_MESSAGE_TEMPLATE
                # Use empty name if template doesn't contain {name} variable
                name_value = "" if "{name}" not in template else "there"
                message = template.format(
                    name=name_value,
                    company=target_data['company'],
                    role=target_data['target_role'],
                    sector=target_data['sector']
                )
                
                # Enter message (LinkedIn has a character limit)
                note_field = self.driver.find_element(By.ID, "custom-message")
                note_field.send_keys(message[:300])  # LinkedIn note limit
                
                # Send request with note
                send_button = self.driver.find_element(
                    By.XPATH, 
                    "//button[contains(@aria-label, 'Send now') or contains(@aria-label, 'Send')]"
                )
                send_button.click()
                
                result['success'] = True
                result['message'] = "Connection request sent with note"
                logger.info(f"Sent connection request to {target_data['company']} - {target_data['target_role']}")
                
            except TimeoutException:
                # Send without note if note option not available
                try:
                    send_button = self.driver.find_element(
                        By.XPATH,
                        "//button[contains(@aria-label, 'Send') or contains(text(), 'Send')]"
                    )
                    send_button.click()
                    result['success'] = True
                    result['message'] = "Connection request sent without note"
                    logger.info(f"Sent connection request (no note) to {target_data['company']} - {target_data['target_role']}")
                except NoSuchElementException:
                    result['message'] = "Could not complete connection request"
            
            time.sleep(config.DELAY_BETWEEN_CONNECTIONS)
            
        except Exception as e:
            result['message'] = f"Error: {str(e)}"
            logger.error(f"Connection request error: {str(e)}")
        
        return result
    
    def close(self):
        """Close the browser and cleanup."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
