"""Email finder service integrations."""

import httpx
from typing import Optional, Dict
from config import settings


class EmailFinderService:
    """Service for finding and validating emails."""
    
    @staticmethod
    async def find_email_hunter(full_name: str, company_domain: str) -> Dict:
        """
        Find email using Hunter.io API.
        
        Args:
            full_name: Full name of the person
            company_domain: Company domain (e.g., google.com)
            
        Returns:
            Dict with email, verified, and confidence fields
        """
        if not settings.HUNTER_API_KEY:
            return {"email": None, "verified": False, "confidence": None}
        
        # Split name
        name_parts = full_name.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "domain": company_domain,
            "first_name": first_name,
            "last_name": last_name,
            "api_key": settings.HUNTER_API_KEY
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("data") and data["data"].get("email"):
                        return {
                            "email": data["data"]["email"],
                            "verified": data["data"].get("verification", {}).get("status") == "valid",
                            "confidence": data["data"].get("confidence")
                        }
        except Exception as e:
            print(f"Hunter.io error: {e}")
        
        return {"email": None, "verified": False, "confidence": None}
    
    @staticmethod
    def generate_email_patterns(full_name: str, company_domain: str) -> list:
        """
        Generate likely email patterns.
        
        Args:
            full_name: Full name of the person
            company_domain: Company domain
            
        Returns:
            List of possible email addresses
        """
        name_parts = full_name.lower().split()
        if not name_parts:
            return []
        
        first = name_parts[0]
        last = name_parts[-1] if len(name_parts) > 1 else ""
        
        patterns = []
        if first and last:
            patterns.extend([
                f"{first}.{last}@{company_domain}",
                f"{first}{last}@{company_domain}",
                f"{first}@{company_domain}",
                f"{first[0]}{last}@{company_domain}",
                f"{last}@{company_domain}",
            ])
        elif first:
            patterns.append(f"{first}@{company_domain}")
        
        return patterns
    
    @staticmethod
    async def find_email(full_name: str, company_domain: str) -> Dict:
        """
        Find email using available services.
        
        Args:
            full_name: Full name of the person
            company_domain: Company domain
            
        Returns:
            Dict with email, verified, and confidence fields
        """
        # Try Hunter.io first
        result = await EmailFinderService.find_email_hunter(full_name, company_domain)
        
        if result.get("email"):
            return result
        
        # If no email found, return patterns as suggestions
        patterns = EmailFinderService.generate_email_patterns(full_name, company_domain)
        if patterns:
            return {
                "email": patterns[0],  # Return most likely pattern
                "verified": False,
                "confidence": "pattern",
                "alternatives": patterns[1:]
            }
        
        return {"email": None, "verified": False, "confidence": None}
