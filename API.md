# Smart Outreach Dashboard - API Documentation

## Base URL
```
http://localhost:8000
```

## Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

### Register User
**POST** `/api/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "company": "Acme Corp",
  "position": "Sales Manager"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "company": "Acme Corp",
  "position": "Sales Manager",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Login
**POST** `/api/auth/login`

Login and receive access token.

**Request Body:** (form-urlencoded)
```
username=user@example.com
password=securepassword
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User
**GET** `/api/auth/me`

Get authenticated user information.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "company": "Acme Corp",
  "position": "Sales Manager",
  "created_at": "2024-01-15T10:00:00Z"
}
```

## Prospects

### List Prospects
**GET** `/api/prospects`

Get all prospects for the authenticated user.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)
- `status` (optional): Filter by status (new, contacted, connected, replied, qualified, unqualified, dead)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "company_id": 1,
    "full_name": "Jane Smith",
    "first_name": "Jane",
    "last_name": "Smith",
    "position": "Software Engineer",
    "email": "jane.smith@company.com",
    "email_verified": true,
    "linkedin_url": "https://linkedin.com/in/janesmith",
    "sector": "Technology",
    "custom_tags": "hot-lead,follow-up",
    "status": "new",
    "last_contacted": null,
    "added_date": "2024-01-15T10:00:00Z",
    "notes": "Met at conference"
  }
]
```

### Create Prospect
**POST** `/api/prospects`

Create a new prospect.

**Request Body:**
```json
{
  "full_name": "Jane Smith",
  "first_name": "Jane",
  "last_name": "Smith",
  "position": "Software Engineer",
  "email": "jane.smith@company.com",
  "linkedin_url": "https://linkedin.com/in/janesmith",
  "company_name": "Tech Corp",
  "sector": "Technology",
  "custom_tags": "hot-lead",
  "notes": "Met at conference"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "company_id": 1,
  "full_name": "Jane Smith",
  "status": "new",
  "added_date": "2024-01-15T10:00:00Z",
  ...
}
```

### Get Prospect
**GET** `/api/prospects/{prospect_id}`

Get a specific prospect by ID.

**Response:** `200 OK` (same format as create)

### Update Prospect
**PUT** `/api/prospects/{prospect_id}`

Update prospect information.

**Request Body:**
```json
{
  "status": "contacted",
  "notes": "Sent connection request",
  "last_contacted": "2024-01-15T10:00:00Z"
}
```

### Delete Prospect
**DELETE** `/api/prospects/{prospect_id}`

Delete a prospect.

**Response:** `200 OK`
```json
{
  "message": "Prospect deleted successfully"
}
```

### Import CSV
**POST** `/api/prospects/import-csv`

Import prospects from CSV file.

**Request:** Multipart form data
- `file`: CSV file

**Response:** `200 OK`
```json
{
  "message": "CSV import completed",
  "imported": 45,
  "skipped": 5,
  "errors": []
}
```

### Find Email
**POST** `/api/prospects/find-email`

Find email using Hunter.io API.

**Request Body:**
```json
{
  "full_name": "Jane Smith",
  "company_domain": "techcorp.com"
}
```

**Response:** `200 OK`
```json
{
  "email": "jane.smith@techcorp.com",
  "verified": true,
  "confidence": 95
}
```

## Templates

### List Templates
**GET** `/api/templates`

Get all templates for authenticated user.

**Query Parameters:**
- `category` (optional): Filter by category

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "LinkedIn Connection Request",
    "category": "linkedin_connection",
    "content": "Hi {first_name}, I noticed...",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": null,
    "times_used": 12
  }
]
```

### Create Template
**POST** `/api/templates`

Create a new template.

**Request Body:**
```json
{
  "title": "LinkedIn Connection Request",
  "category": "linkedin_connection",
  "content": "Hi {first_name}, I noticed you work at {company}..."
}
```

### Update Template
**PUT** `/api/templates/{template_id}`

Update template.

### Delete Template
**DELETE** `/api/templates/{template_id}`

Delete template.

### Compose Message
**POST** `/api/templates/compose`

Compose message from template with prospect data.

**Request Body:**
```json
{
  "template_id": 1,
  "prospect_id": 1,
  "custom_note": "We met at the conference"
}
```

**Response:** `200 OK`
```json
{
  "message": "Hi Jane, I noticed you work at Tech Corp. We met at the conference...",
  "character_count": 145
}
```

## Activities

### List Activities
**GET** `/api/activities`

Get activity log.

**Query Parameters:**
- `skip`, `limit`: Pagination
- `activity_type` (optional): Filter by type

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "prospect_id": 1,
    "activity_type": "connection_sent",
    "description": "Sent LinkedIn connection request",
    "created_at": "2024-01-15T10:00:00Z"
  }
]
```

### Create Activity
**POST** `/api/activities`

Log a new activity.

**Request Body:**
```json
{
  "prospect_id": 1,
  "activity_type": "email_sent",
  "description": "Sent initial outreach email"
}
```

### Today's Activity Count
**GET** `/api/activities/today-count`

Get today's activity statistics.

**Response:** `200 OK`
```json
{
  "count": 12,
  "limit": 20,
  "remaining": 8
}
```

## Analytics

### Dashboard Metrics
**GET** `/api/analytics/dashboard`

Get dashboard metrics.

**Response:** `200 OK`
```json
{
  "total_prospects": 150,
  "new_prospects": 45,
  "contacted": 65,
  "connected": 48,
  "replied": 23,
  "qualified": 12,
  "connection_acceptance_rate": 73.8,
  "daily_activity_count": 12,
  "daily_limit": 20
}
```

### Activity Stats
**GET** `/api/analytics/activity-stats`

Get activity statistics over time.

**Query Parameters:**
- `days` (optional): Number of days to include (default: 30)

**Response:** `200 OK`
```json
[
  {
    "date": "2024-01-15",
    "count": 15
  },
  {
    "date": "2024-01-16",
    "count": 18
  }
]
```

### Pipeline Stats
**GET** `/api/analytics/pipeline-stats`

Get pipeline distribution.

**Response:** `200 OK`
```json
{
  "new": 45,
  "contacted": 65,
  "connected": 48,
  "replied": 23,
  "qualified": 12,
  "unqualified": 8,
  "dead": 5
}
```

## Error Responses

All endpoints may return the following errors:

**400 Bad Request**
```json
{
  "detail": "Invalid input data"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

**404 Not Found**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- Email finder API calls are limited by your API provider
- Daily activity tracking enforces configurable limits
- No global rate limiting on API endpoints

## Authentication Flow

1. Register: `POST /api/auth/register`
2. Login: `POST /api/auth/login` → Receive token
3. Use token in all subsequent requests:
   ```
   Authorization: Bearer {token}
   ```
4. Token expires after 7 days (configurable)

## Best Practices

1. **Always include Authorization header** for protected endpoints
2. **Handle 401 errors** by redirecting to login
3. **Use pagination** for large datasets
4. **Check activity limits** before bulk operations
5. **Validate CSV format** before importing
6. **Store tokens securely** (never in localStorage for production)

---

For more details, visit the interactive documentation at http://localhost:8000/docs
