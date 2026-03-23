# Quick Reference Guide

## 🚀 Getting Started in 5 Minutes

### 1. Start the Application
```bash
./start.sh
```
Or manually:
```bash
# Terminal 1 - Backend
cd backend && pip install -r requirements.txt && python main.py

# Terminal 2 - Frontend  
cd frontend && npm install && npm run dev
```

### 2. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. First Time Setup
1. Click "Register" → Create account
2. Login with credentials
3. Import `sample_prospects.csv` or add prospects manually
4. Create templates or use sample templates
5. Start managing your outreach!

## 📋 Common Tasks

### Add a Prospect
1. Go to **Prospects** page
2. Click **"Add Prospect"**
3. Fill in: Name, Company, Position, Email
4. Click **"Add Prospect"**

### Import CSV
1. Go to **Prospects** page
2. Click **"Import CSV"**
3. Drag & drop or browse for CSV file
4. Click **"Import CSV"**

### Create Template
1. Go to **Templates** page
2. Click **"New Template"**
3. Enter title and choose category
4. Write message with variables: `{first_name}`, `{company}`, etc.
5. Save template

### Update Prospect Status
1. Find prospect card
2. Use status dropdown at bottom
3. Select new status (New, Contacted, Connected, etc.)

### Copy Message
1. On prospect card, click **"Copy Message"**
2. Message with prospect details copied to clipboard
3. Paste in LinkedIn or email

## 🔑 Keyboard Shortcuts

- `Ctrl/Cmd + K` - Global search (coming soon)
- `Esc` - Close modals
- `Tab` - Navigate form fields

## 💡 Pro Tips

### CSV Import
- Required columns: `company`, `name` or `full_name`
- Optional: `sector`, `desired_role`, `email`, `linkedin_url`
- File must be `.csv` format
- UTF-8 encoding recommended

### Email Finding
1. Set `HUNTER_API_KEY` in `backend/.env`
2. Use "Find Email" on prospect without email
3. System will search and verify
4. Free tier: 50 requests/month

### Templates
- Use `{first_name}` for personalization
- LinkedIn connection: max 300 characters
- Test variables before using
- Copy successful templates

### Daily Limits
- Default: 20 activities/day
- Change in `backend/.env`: `MAX_DAILY_OUTREACH=30`
- Dashboard shows progress bar
- Red warning at 100%

## 🎯 Status Pipeline

```
NEW → CONTACTED → CONNECTED → REPLIED → QUALIFIED
```

Use status to track:
- **New**: Just added
- **Contacted**: Sent connection/email
- **Connected**: Accepted on LinkedIn
- **Replied**: Got a response
- **Qualified**: Potential opportunity
- **Unqualified**: Not a fit
- **Dead**: No response/closed

## 🔧 Quick Troubleshooting

### Backend won't start
```bash
# Check port 8000
lsof -ti:8000 | xargs kill -9
cd backend && python main.py
```

### Frontend won't start
```bash
# Check port 3000
lsof -ti:3000 | xargs kill -9
cd frontend && npm run dev
```

### Can't login
- Clear browser cache
- Check backend is running
- Verify credentials
- Try registering new account

### CSV import fails
- Check file format (must be .csv)
- Verify required columns exist
- Check for special characters
- Try sample file first

### Email finder not working
- Verify `HUNTER_API_KEY` in `.env`
- Check API quota at hunter.io
- Restart backend after adding key
- Try with known company domain

## 📊 Sample Variables

```
{first_name}    → John
{last_name}     → Smith  
{full_name}     → John Smith
{company}       → Google
{position}      → Software Engineer
{sector}        → Technology
{my_name}       → Your Name
{my_company}    → Your Company
{my_position}   → Your Position
{custom_note}   → Custom text
```

## 🐳 Docker Quick Start

```bash
# Start with Docker
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

## 📱 API Quick Reference

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -F "username=user@example.com" \
  -F "password=pass123"
```

### Prospects
```bash
# List prospects
curl http://localhost:8000/api/prospects \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create prospect
curl -X POST http://localhost:8000/api/prospects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"John Doe","company_name":"Acme Corp"}'
```

### Templates
```bash
# List templates
curl http://localhost:8000/api/templates \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create template
curl -X POST http://localhost:8000/api/templates \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Template","content":"Hi {first_name}..."}'
```

## 🆘 Support

- **Documentation**: README.md, SETUP.md, API.md
- **API Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Email**: Check repository for contact

## 📈 Usage Workflow

1. **Import Prospects** → CSV or manual entry
2. **Create Templates** → Write messages with variables
3. **Update Status** → Track progress through pipeline
4. **Monitor Analytics** → View metrics and charts
5. **Daily Activity** → Follow 20/day limit
6. **Review & Optimize** → Check acceptance rates

---

**Happy Networking! 🚀**
