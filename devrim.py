"""Main application for LinkedIn connection automation tool."""

import argparse
import logging
import sys
from pathlib import Path

from csv_parser import parse_csv_file, create_example_csv, CSVParserError
from linkedin_connector import LinkedInConnector, LinkedInAutomationError
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('devrim.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def print_banner():
    """Print application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                      DEVRIM                           ║
    ║          LinkedIn Connection Automation Tool          ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def process_csv_file(csv_path: str, message_template: str = None, dry_run: bool = False):
    """
    Process CSV file and send connection requests.
    
    Args:
        csv_path: Path to CSV file
        message_template: Custom message template
        dry_run: If True, only parse CSV without sending requests
    """
    try:
        # Parse CSV file
        logger.info(f"Parsing CSV file: {csv_path}")
        company_data = parse_csv_file(csv_path)
        
        print(f"\n✓ Successfully parsed {len(company_data)} entries from CSV\n")
        
        # Display parsed data
        print("Companies and roles to target:")
        print("-" * 60)
        for idx, entry in enumerate(company_data, 1):
            print(f"{idx}. {entry['company']} - {entry['target_role']} ({entry['sector']})")
        print("-" * 60)
        
        if dry_run:
            print("\n[DRY RUN MODE] - No connection requests will be sent")
            return
        
        # Confirm before proceeding
        print(f"\nThis will attempt to send {len(company_data)} connection requests.")
        response = input("Do you want to proceed? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("Operation cancelled by user.")
            return
        
        # Initialize LinkedIn connector
        logger.info("Initializing LinkedIn connector")
        connector = LinkedInConnector()
        
        # Login to LinkedIn
        print("\nLogging in to LinkedIn...")
        if not connector.login():
            print("❌ Failed to login to LinkedIn. Please check your credentials.")
            return
        
        print("✓ Successfully logged in to LinkedIn\n")
        
        # Process each entry
        results = {'success': 0, 'failed': 0}
        max_connections = min(len(company_data), config.MAX_CONNECTIONS_PER_SESSION)
        
        print(f"Sending connection requests (max {max_connections} per session)...\n")
        
        for idx, entry in enumerate(company_data[:max_connections], 1):
            print(f"[{idx}/{max_connections}] Processing: {entry['company']} - {entry['target_role']}")
            
            result = connector.send_connection_request(entry, message_template)
            
            if result['success']:
                results['success'] += 1
                print(f"  ✓ {result['message']}")
            else:
                results['failed'] += 1
                print(f"  ✗ {result['message']}")
            
            print()
        
        # Close browser
        connector.close()
        
        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total processed: {max_connections}")
        print(f"Successful: {results['success']}")
        print(f"Failed: {results['failed']}")
        print("=" * 60)
        
        if len(company_data) > max_connections:
            remaining = len(company_data) - max_connections
            print(f"\nNote: {remaining} entries were not processed due to session limit.")
            print(f"To process remaining entries, run the tool again with a CSV")
            print(f"containing only the unprocessed entries.")
        
    except CSVParserError as e:
        logger.error(f"CSV parsing error: {str(e)}")
        print(f"\n❌ CSV Error: {str(e)}")
        sys.exit(1)
        
    except LinkedInAutomationError as e:
        logger.error(f"LinkedIn automation error: {str(e)}")
        print(f"\n❌ LinkedIn Error: {str(e)}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user.")
        if 'connector' in locals():
            connector.close()
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='Devrim - LinkedIn Connection Automation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a CSV file
  python devrim.py companies.csv
  
  # Create an example CSV file
  python devrim.py --create-example
  
  # Dry run (parse CSV without sending requests)
  python devrim.py companies.csv --dry-run
  
  # Use custom message template
  python devrim.py companies.csv --message "Hi {name}, interested in {sector}!"
        """
    )
    
    parser.add_argument(
        'csv_file',
        nargs='?',
        help='Path to CSV file with company data'
    )
    
    parser.add_argument(
        '--create-example',
        action='store_true',
        help='Create an example CSV file'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse CSV without sending connection requests'
    )
    
    parser.add_argument(
        '--message',
        type=str,
        help='Custom message template (variables: {name}, {company}, {role}, {sector})'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Create example CSV
    if args.create_example:
        print("Creating example CSV file...")
        create_example_csv()
        print("✓ Example CSV created: example_companies.csv")
        print("\nEdit this file with your target companies and roles, then run:")
        print("  python devrim.py example_companies.csv")
        return
    
    # Validate CSV file argument
    if not args.csv_file:
        parser.print_help()
        print("\n❌ Error: Please provide a CSV file or use --create-example")
        sys.exit(1)
    
    if not Path(args.csv_file).exists():
        print(f"❌ Error: File not found: {args.csv_file}")
        sys.exit(1)
    
    # Process CSV file
    process_csv_file(args.csv_file, args.message, args.dry_run)


if __name__ == '__main__':
    main()
