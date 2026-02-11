# Smart Outreach Dashboard

A professional tool for managing LinkedIn and email outreach campaigns with intelligent lead tracking, message templates, and analytics.

## 🌟 Features

### Data Collection & Enrichment
- **Multiple Input Methods**: CSV upload, manual entry, and bulk import
- **Email Finder Integration**: Hunter.io API integration for finding professional emails
- **Email Pattern Generation**: Auto-generate likely email patterns
- **Smart Validation**: Email verification and duplicate detection

### Intelligent Dashboard
- **Modern UI**: Clean, Notion-style interface with dark/light mode
- **Pipeline View**: Visual prospect management across multiple stages
- **Prospect Cards**: Rich prospect information with quick actions
- **Status Tracking**: New → Contacted → Connected → Replied → Qualified

### Message Management
- **Template Library**: Pre-built templates for LinkedIn and email
- **Smart Variables**: Dynamic content with merge fields
- **Character Counter**: LinkedIn message limits tracking

### Analytics & Reporting
- **Dashboard Metrics**: Total prospects, connection rates, activity stats
- **Visual Charts**: Activity graphs and pipeline distribution
- **Daily Tracking**: Monitor your outreach activities with daily limits

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python main.py
```

API: http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:3000

### Quick Start with Script

```bash
./start.sh
```

## 📊 CSV Import Format

| Column | Required | Description |
|--------|----------|-------------|
| company | Yes | Company name |
| name or full_name | Yes | Full name |
| sector | No | Industry sector |
| desired_role or position | No | Job title |
| email | No | Email address |
| linkedin_url | No | LinkedIn URL |

See `sample_prospects.csv` for an example.

## 🛠️ Tech Stack

**Backend**: FastAPI, SQLAlchemy, JWT, Pydantic  
**Frontend**: React 18, TypeScript, TailwindCSS, React Query, Recharts

## 📝 API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎨 Features Overview

### MVP Features ✅
- Prospect database with CSV import
- Email finder integration (Hunter.io)
- Message templates with variables
- Pipeline view with status management
- Quick actions (copy message, open LinkedIn)
- Basic analytics and metrics
- Activity tracking with daily limits
- Dark/Light mode toggle
- Authentication system

### Future Enhancements
- Chrome extension for LinkedIn
- AI message generation (Anthropic API)
- Email sending integration (Gmail API)
- Advanced analytics and reporting
- Team collaboration features
- Email sequence automation

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

## ⚠️ Disclaimer

Use responsibly and respect LinkedIn's Terms of Service.

---

Built with ❤️ for professional outreach and networking
