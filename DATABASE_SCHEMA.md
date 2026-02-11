# Database Schema Diagram

## Smart Outreach Dashboard - Database Structure

### Tables Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     SMART OUTREACH DATABASE                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    USERS     │         │  COMPANIES   │         │  TEMPLATES   │
├──────────────┤         ├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │         │ id (PK)      │
│ email        │         │ name         │         │ user_id (FK) │
│ hashed_pwd   │         │ domain       │         │ title        │
│ full_name    │         │ sector       │         │ category     │
│ company      │         │ notes        │         │ content      │
│ position     │         │ created_at   │         │ times_used   │
│ created_at   │         └──────────────┘         │ created_at   │
└──────────────┘                │                 └──────────────┘
       │                        │                        │
       │                        │                        │
       │         ┌──────────────▼──────────────┐         │
       │         │        PROSPECTS            │         │
       │         ├─────────────────────────────┤         │
       └────────►│ id (PK)                     │         │
                 │ user_id (FK) ───────────────┼─────────┘
                 │ company_id (FK)             │
                 │ full_name                   │
                 │ first_name, last_name       │
                 │ position                    │
                 │ email, email_verified       │
                 │ linkedin_url                │
                 │ sector, custom_tags         │
                 │ status                      │
                 │ last_contacted              │
                 │ added_date, notes           │
                 └─────────────────────────────┘
                                │
                                │
       ┌────────────────────────┴────────────────────┐
       │                                             │
       ▼                                             ▼
┌──────────────┐                          ┌──────────────────┐
│  ACTIVITIES  │                          │ EMAIL_SEQUENCES  │
├──────────────┤                          ├──────────────────┤
│ id (PK)      │                          │ id (PK)          │
│ user_id (FK) │                          │ prospect_id (FK) │
│ prospect_id  │                          │ template_id (FK) │
│ activity_type│                          │ sequence_number  │
│ description  │                          │ scheduled_date   │
│ created_at   │                          │ sent_date        │
└──────────────┘                          │ status           │
                                          │ opened, clicked  │
                                          └──────────────────┘
```

### Relationships

1. **Users → Prospects**: One-to-Many
   - Each user can have multiple prospects
   - Prospects belong to one user

2. **Companies → Prospects**: One-to-Many
   - Each company can have multiple prospects
   - Prospects are associated with one company

3. **Users → Templates**: One-to-Many
   - Each user can create multiple templates
   - Templates belong to one user

4. **Users → Activities**: One-to-Many
   - Each user can have multiple activities
   - Activities belong to one user

5. **Prospects → Activities**: One-to-Many
   - Each prospect can have multiple activities
   - Activities can be linked to a prospect

6. **Prospects → Email Sequences**: One-to-Many
   - Each prospect can have multiple email sequences
   - Sequences are linked to one prospect

### Status Flow (Prospects)

```
NEW → CONTACTED → CONNECTED → REPLIED → QUALIFIED
  ↓       ↓           ↓          ↓           ↓
  └───────┴───────────┴──────────┴──────→ UNQUALIFIED
                                               ↓
                                             DEAD
```

### Activity Types

- `prospect_added` - New prospect created
- `csv_import` - Bulk CSV import
- `connection_sent` - LinkedIn connection request sent
- `email_sent` - Email sent to prospect
- `note_added` - Note added to prospect
- `status_changed` - Prospect status updated

### Template Categories

- `linkedin_connection` - LinkedIn connection requests
- `linkedin_followup` - LinkedIn follow-up messages
- `email_initial` - Initial email outreach
- `email_followup` - Follow-up emails

### Indexes

- Users: `email` (unique)
- Companies: `name`, `domain`
- Prospects: `user_id`, `email`, `status`
- Templates: `user_id`, `category`
- Activities: `user_id`, `prospect_id`, `created_at`

---

This schema supports:
- Multi-user system with data isolation
- Company-based prospect grouping
- Template reusability
- Activity logging and tracking
- Email sequence automation
- Status pipeline management
