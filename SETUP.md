# Setup Guide for Smart Outreach Dashboard

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Backend Configuration](#backend-configuration)
3. [Frontend Configuration](#frontend-configuration)
4. [API Keys Setup](#api-keys-setup)
5. [First User Registration](#first-user-registration)
6. [Importing Prospects](#importing-prospects)
7. [Creating Templates](#creating-templates)
8. [Troubleshooting](#troubleshooting)

## Initial Setup

### System Requirements
- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn
- Git (for cloning the repository)

### Quick Installation

#### Option 1: Using the Start Script (Recommended)
```bash
./start.sh
```

This script will:
- Set up Python virtual environment
- Install all dependencies
- Start both backend and frontend servers
- Open the application in your browser

#### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

**Frontend (in a new terminal):**
```bash
cd frontend
npm install
npm run dev
```

## Backend Configuration

### Environment Variables

Edit `backend/.env` with your settings:

```env
# Application
APP_NAME=Smart Outreach Dashboard
DEBUG=True

# Database
DATABASE_URL=sqlite:///./outreach.db

# Security - CHANGE THESE IN PRODUCTION
SECRET_KEY=your-very-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# API Keys (Optional but recommended)
HUNTER_API_KEY=your_hunter_api_key
APOLLO_API_KEY=your_apollo_api_key
CLEARBIT_API_KEY=your_clearbit_api_key

# Rate Limiting
MAX_DAILY_OUTREACH=20

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Database Setup

The application uses SQLite by default for easy setup. The database file will be created automatically when you first start the backend.

For production, you can switch to PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Frontend Configuration

The frontend connects to the backend API automatically. If you need to change the API URL:

Create `frontend/.env.local`:
```env
VITE_API_URL=http://localhost:8000
```

## API Keys Setup

### Hunter.io (Email Finder)

1. Sign up at https://hunter.io
2. Go to API section in your dashboard
3. Copy your API key
4. Add to `backend/.env`:
   ```env
   HUNTER_API_KEY=your_key_here
   ```

Free tier: 50 requests/month

### Apollo.io (Alternative Email Finder)

1. Sign up at https://apollo.io
2. Go to Settings → Integrations → API
3. Generate an API key
4. Add to `backend/.env`:
   ```env
   APOLLO_API_KEY=your_key_here
   ```

### Clearbit (Company Enrichment)

1. Sign up at https://clearbit.com
2. Get your API key from dashboard
3. Add to `backend/.env`:
   ```env
   CLEARBIT_API_KEY=your_key_here
   ```

## First User Registration

1. Start the application
2. Navigate to http://localhost:3000
3. Click "Register" on the login page
4. Fill in your details:
   - Email address (required)
   - Password (required)
   - Full name (optional)
   - Company (optional)
   - Position (optional)
5. Click "Create account"
6. Login with your credentials

## Importing Prospects

### Method 1: CSV Import

1. Prepare your CSV file with required columns:
   - `company` (required)
   - `name` or `full_name` (required)
   - `sector` (optional)
   - `desired_role` or `position` (optional)
   - `email` (optional)
   - `linkedin_url` (optional)

2. Example CSV (`sample_prospects.csv` is provided):
   ```csv
   company,name,sector,desired_role,email,linkedin_url
   Google,John Smith,Technology,Software Engineer,,https://linkedin.com/in/johnsmith
   Microsoft,Jane Doe,Technology,Product Manager,jane@microsoft.com,
   ```

3. In the application:
   - Go to "Prospects" page
   - Click "Import CSV"
   - Drag and drop or browse for your CSV file
   - Click "Import"
   - Review imported prospects

### Method 2: Manual Entry

1. Go to "Prospects" page
2. Click "Add Prospect"
3. Fill in prospect details
4. Click "Add Prospect"

### Email Finding

For prospects without emails:
1. View the prospect card
2. Use the email finder integration (requires Hunter.io API key)
3. The system will attempt to find and verify the email

## Creating Templates

### Step 1: Navigate to Templates

Go to the "Templates" page from the sidebar.

### Step 2: Create a New Template

1. Click "New Template"
2. Enter template details:
   - **Title**: Give your template a descriptive name
   - **Category**: Choose from:
     - LinkedIn Connection
     - LinkedIn Follow-up
     - Email Initial
     - Email Follow-up
   - **Content**: Write your message with variables

### Step 3: Use Variables

Available variables in templates:
- `{first_name}` - Prospect's first name
- `{last_name}` - Prospect's last name
- `{full_name}` - Prospect's full name
- `{company}` - Prospect's company
- `{position}` - Prospect's position
- `{sector}` - Industry sector
- `{my_name}` - Your full name
- `{my_company}` - Your company
- `{my_position}` - Your position
- `{custom_note}` - Custom note field

### Example Template

**LinkedIn Connection Request:**
```
Hi {first_name},

I noticed you work at {company} as a {position}. I'm particularly interested in the {sector} industry and would love to connect.

Best regards,
{my_name}
```

**Character Limit**: LinkedIn connection messages have a 300-character limit. The template system shows character count in real-time.

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

**Database errors:**
```bash
# Delete and recreate database
cd backend
rm outreach.db
python main.py  # Will create new database
```

**Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# Change port in vite.config.ts or kill the process
lsof -ti:3000 | xargs kill -9
```

**Node modules issues:**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

### Authentication Issues

**Can't login:**
- Check that backend is running on port 8000
- Clear browser localStorage: `localStorage.clear()`
- Check browser console for errors

**Token expired:**
- Login again to get a new token
- Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env` if needed

### CSV Import Issues

**Invalid CSV format:**
- Ensure file has `.csv` extension
- Check that required columns exist: `company`, `name`/`full_name`
- Verify CSV is UTF-8 encoded

**Duplicates skipped:**
- System prevents duplicate prospects by name
- This is intentional to avoid data duplication

### Email Finder Not Working

**No API key:**
- Add Hunter.io API key to `backend/.env`
- Restart backend server

**API rate limit:**
- Check your Hunter.io account for remaining quota
- Free tier: 50 requests/month
- Consider upgrading or using Apollo.io as backup

### General Debugging

**Check logs:**
```bash
# Backend logs (in terminal running backend)
# Frontend logs (browser console)
```

**API Documentation:**
Visit http://localhost:8000/docs for interactive API documentation

**Database Browser:**
Use DB Browser for SQLite to inspect the database file

## Support

For additional help:
1. Check the main README.md
2. Review API documentation at http://localhost:8000/docs
3. Open an issue on GitHub

---

Happy outreaching! 🚀
