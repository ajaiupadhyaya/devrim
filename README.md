# Devrim - LinkedIn Connection Automation Tool

A Python-based tool that automates LinkedIn connection requests based on a CSV file containing target companies, sectors, and roles. Send personalized connection messages to people in your target roles at specific companies.

## Features

- 📊 **CSV-based input**: Upload a CSV file with company, sector, and target role information
- 🤖 **Automated connections**: Automatically search and send connection requests on LinkedIn
- 💬 **Personalized messages**: Send customized messages with each connection request
- ⚙️ **Configurable**: Customize message templates, connection limits, and delays
- 🛡️ **Safe**: Built-in rate limiting and session management
- 📝 **Logging**: Comprehensive logging for tracking operations

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- LinkedIn account

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ajaiupadhyaya/devrim.git
cd devrim
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your LinkedIn credentials:
```bash
cp .env.example .env
```

Edit the `.env` file and add your LinkedIn credentials:
```
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```

## Usage

### Quick Start

1. **Create an example CSV file**:
```bash
python devrim.py --create-example
```

This creates `example_companies.csv` with sample data.

2. **Edit the CSV file** with your target companies and roles:
```csv
company,sector,target_role
Google,Technology,Software Engineer
Microsoft,Technology,Senior Developer
Amazon,E-commerce,DevOps Engineer
```

3. **Run the tool**:
```bash
python devrim.py example_companies.csv
```

### CSV File Format

The CSV file must have exactly 3 columns in this order:
1. **company**: Company name (e.g., "Google", "Microsoft")
2. **sector**: Industry sector (e.g., "Technology", "Finance")
3. **target_role**: Job title to target (e.g., "Software Engineer", "Product Manager")

Example:
```csv
company,sector,target_role
Google,Technology,Software Engineer
Apple,Technology,iOS Developer
Goldman Sachs,Finance,Investment Analyst
```

### Command Line Options

```bash
# Basic usage
python devrim.py companies.csv

# Dry run (validate CSV without sending requests)
python devrim.py companies.csv --dry-run

# Custom message template
python devrim.py companies.csv --message "Hi {name}, interested in {company}!"

# Create example CSV
python devrim.py --create-example
```

### Custom Message Templates

You can customize the connection message in two ways:

1. **Via .env file**:
```
MESSAGE_TEMPLATE=Hi {name}, I noticed you work at {company} as a {role}. I'm interested in the {sector} sector and would love to connect!
```

2. **Via command line**:
```bash
python devrim.py companies.csv --message "Hi {name}, I see you're at {company}. Let's connect!"
```

**Available variables**:
- `{name}`: Person's name (defaults to "there" in search results)
- `{company}`: Company name from CSV
- `{role}`: Target role from CSV
- `{sector}`: Sector from CSV

**Note**: LinkedIn limits connection notes to 300 characters.

## Configuration

Edit the `.env` file to customize settings:

```bash
# LinkedIn Credentials
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# Connection Settings
MAX_CONNECTIONS_PER_SESSION=20  # Max connections per run
DELAY_BETWEEN_CONNECTIONS=5      # Seconds between requests

# Message Template
MESSAGE_TEMPLATE=Hi {name}, I noticed you work at {company}...

# Browser Settings
HEADLESS_MODE=False  # Set to True to hide browser window
```

## Safety Features

- **Rate Limiting**: Default limit of 20 connections per session (configurable)
- **Delays**: Built-in delays between requests to avoid triggering LinkedIn's rate limits
- **Session Management**: Automatic browser cleanup
- **Logging**: All actions are logged to `devrim.log`

## Best Practices

1. **Start Small**: Test with a small CSV file (5-10 entries) first
2. **Reasonable Limits**: Keep MAX_CONNECTIONS_PER_SESSION low (10-20)
3. **Personalize Messages**: Customize your message template for better response rates
4. **Respect Rate Limits**: Don't run the tool too frequently
5. **Monitor Logs**: Check `devrim.log` for any issues

## Troubleshooting

### Login Issues
- Verify your credentials in the `.env` file
- If using 2FA, you may need to handle the verification manually
- LinkedIn may require CAPTCHA verification on first login

### Connection Request Issues
- LinkedIn may limit your connection requests if you exceed daily limits
- Some users may have restricted connection settings
- Try increasing `DELAY_BETWEEN_CONNECTIONS` if requests are failing

### Browser Issues
- Ensure Chrome browser is installed
- Try setting `HEADLESS_MODE=False` to see what's happening
- Check `devrim.log` for detailed error messages

## Project Structure

```
devrim/
├── devrim.py              # Main application
├── linkedin_connector.py  # LinkedIn automation logic
├── csv_parser.py          # CSV parsing and validation
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment configuration
├── .gitignore            # Git ignore rules
├── example_companies.csv # Example CSV file
└── README.md             # This file
```

## Security Notes

- **Never commit** your `.env` file with real credentials
- Use environment variables for sensitive data
- The `.gitignore` file is configured to exclude `.env` files
- LinkedIn credentials are only used locally and never transmitted to third parties

## Limitations

- LinkedIn may change their UI, which could break automation
- Daily connection request limits apply (LinkedIn's policy)
- Not all connection requests will include a note (depends on relationship)
- CAPTCHA or security checks may require manual intervention

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This tool automates interactions with LinkedIn. Use it responsibly and in accordance with LinkedIn's Terms of Service. Excessive automation may result in account restrictions. The authors are not responsible for any consequences of using this tool.

## Support

For issues and questions, please open an issue on GitHub.
