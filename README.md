# Video Streaming Backend

## Overview

This project is a backend system for video upload, processing, secure streaming, and monetized access control. It is designed for video-on-demand platforms, e-learning systems, and media services.

The implementation focuses on backend architecture, security, RBAC, and business logic. Video encoding and streaming file generation are simulated for backend-focused assessment. In production, this would integrate with object storage (e.g., S3) and an FFmpeg-based HLS/DASH pipeline.




# 1. Clone Repository
git clone https://github.com/sameer75way/video_streaming_backend.git
cd video_streaming_backend

# 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate      # Windows

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Create .env File
touch .env



# In env

DATABASE_URL=postgresql+asyncpg://sameer75:1234@localhost:5432/video_streaming_db

SECRET_KEY=supersecretkey
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

DEFAULT_ADMIN_EMAIL=admin@platform.com
DEFAULT_ADMIN_PASSWORD=Admin@123

RATE_LIMIT_DEFAULT=60
RATE_LIMIT_AUTH=20
RATE_LIMIT_STREAM=20

# 5. Create PostgreSQL Database



# 6. Run Migrations
python -m alembic upgrade head

# 7. Start Server
uvicorn main:app --reload
---

## Features

### Authentication
- Access and refresh token based authentication (JWT)
- Password hashing
- Role-based access control (RBAC)
- Admin-only route protection

### User Roles
- ADMIN
- CREATOR
- VIEWER

Roles are automatically seeded on startup.

### Auto Admin Seeder
On first application startup:
- Roles are created if not present
- A default admin user is created if not present

Default admin credentials are controlled via environment variables:

DEFAULT_ADMIN_EMAIL  
DEFAULT_ADMIN_PASSWORD  

The admin is created only once (idempotent seeding).

---

Default Roles Created Automatically on Startup:
ADMIN
CREATOR
VIEWER

Default Admin Credentials:
Email: admin@platform.com
Password: Admin@123

Core System Capabilities:
- Role Based Access Control (ADMIN, CREATOR, VIEWER)
- JWT Authentication (Access + Refresh Tokens)
- Secure Stream Token (1 minute expiry)
- Video Lifecycle: UPLOADED → PROCESSING → READY
- Soft Delete + Restore
- Paid Video Purchase Flow
- Subscription Access Model
- Revenue Split (80% Creator / 20% Platform)
- Audit Logging Middleware
- Rate Limiting (Auth, Stream, Default)
- Analytics (Views, Unique Views, Likes, Dislikes)

### Video Management
- Video creation (CREATOR)
- Background encoding simulation
- Status lifecycle:
  - UPLOADED
  - PROCESSING
  - READY
- Soft delete
- Restore (ADMIN only)

---

### Secure Streaming
- Short-lived signed streaming tokens
- Token validation before playback
- Access enforcement:
  - Free videos accessible to all
  - Paid videos require purchase or subscription
  - Admin and owner override

---

### Monetization
- One-time video purchase
- Subscription system
- Revenue tracking
- Creator earnings calculation
- Admin revenue overview

---

### Engagement & Analytics
- View tracking
- Unique viewers
- Like / Dislike tracking
- Creator analytics dashboard
- Admin analytics dashboard

---

### Security & Hardening
- Rate limiting (configurable via environment)
- Audit logging of API activity
- Service-layer architecture (no business logic in routes)
- Async database operations
- Alembic migrations
- Soft delete protection

---

## Tech Stack

- FastAPI
- SQLModel / SQLAlchemy (Async)
- PostgreSQL
- Alembic
- JWT authentication

---

## Project Structure

video_streaming_backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│
├── alembic/
├── main.py
├── .env.example
├── requirements.txt
├── README.md
├── .gitignore

---

## Environment Setup

Copy the example file:

cp .env.example .env

Fill required values.

### Example .env fields

DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/video_streaming_db  
SECRET_KEY=your_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=15  
REFRESH_TOKEN_EXPIRE_DAYS=7  

DEFAULT_ADMIN_EMAIL=admin@platform.com  
DEFAULT_ADMIN_PASSWORD=Admin@123  

RATE_LIMIT_DEFAULT=60  
RATE_LIMIT_AUTH=5  
RATE_LIMIT_STREAM=20  

---

## Installation

Create virtual environment and install dependencies:

python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

---

## Database Setup

Create PostgreSQL database manually:

CREATE DATABASE video_streaming_db;

Run migrations:

python -m alembic upgrade head

---

## Run Application

uvicorn main:app --reload --port 2001

Application will start at:

http://127.0.0.1:2001

On first run, default admin is created automatically.

---

## API Routes

### Authentication

POST /api/v1/auth/register  
POST /api/v1/auth/login  
POST /api/v1/auth/refresh  
GET /api/v1/auth/me  

---

### Users (Admin Only)

GET /api/v1/users/  
PATCH /api/v1/users/{user_id}/role  

---

### Videos

POST /api/v1/videos/  
GET /api/v1/videos/  
GET /api/v1/videos/{video_id}  
DELETE /api/v1/videos/{video_id}  
PATCH /api/v1/videos/{video_id}/restore  

---

### Streaming

GET /api/v1/stream/{video_id}  
GET /api/v1/stream/play/{token}  

---

### Payments

POST /api/v1/payments/purchase/{video_id}  
POST /api/v1/payments/subscribe  

---

### Analytics

GET /api/v1/analytics/creator  
GET /api/v1/analytics/admin  

---

### Audit Logs (Admin Only)

GET /api/v1/audit/  

---

## Testing Flow

1. Start server.
2. Login using default admin credentials.
3. Create a CREATOR user.
4. Login as CREATOR and create a video.
5. Wait for encoding simulation to complete.
6. Login as VIEWER and attempt to stream:
   - Free video should work.
   - Paid video should require purchase or subscription.
7. Test purchase flow.
8. Test analytics dashboards.
9. Test rate limiting by reducing values in .env.

---

## Notes

- Video encoding and HLS/DASH generation are simulated.
- In production, integrate:
  - Object storage (e.g., S3)
  - FFmpeg-based HLS/DASH pipeline
  - Distributed worker (e.g., Celery)

