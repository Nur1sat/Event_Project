# JIHC Clubs Activity Web App

A full-stack web application for managing college club activities and student registrations.

## Tech Stack

**Backend:**
- Python 3.10+
- FastAPI (REST API framework)
- SQLAlchemy (ORM)
- SQLite (Database)
- JWT Authentication (python-jose)
- Bcrypt (Password hashing)
- Pydantic (Data validation)

**Frontend:**
- Vue.js 3
- Vue Router (Navigation)
- Pinia (State Management)
- Axios (HTTP Client)
- Vite (Build tool)

---

## 🚀 Backend API Capabilities

### 🔐 Authentication & Authorization

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/auth/register` | POST | Register new student account | Public |
| `/api/auth/admin/register` | POST | Register admin (secret key: `111111`) | Public |
| `/api/auth/login` | POST | Login and get JWT token | Public |

**Features:**
- JWT token-based authentication
- Role-based access control (Student / Admin)
- Password hashing with bcrypt
- Token expiration (24 hours)

---

### 👥 User Management

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/users/me` | GET | Get current user profile | Authenticated |
| `/api/users/me` | PUT | Update current user profile | Authenticated |
| `/api/users/` | GET | List all users | Admin only |

---

### 📅 Event Management

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/events/` | GET | List events (pagination, search, filter) | Authenticated |
| `/api/events/{id}` | GET | Get event details | Authenticated |
| `/api/events/` | POST | Create new event | Admin only |
| `/api/events/{id}` | PUT | Update event | Admin only |
| `/api/events/{id}` | DELETE | Delete event | Admin only |
| `/api/events/{id}/participants` | GET | Get participants list | Admin only |

**Features:**
- Full CRUD operations
- Pagination (`page`, `per_page`)
- Search by title (`search`)
- Filter by status (`status`: upcoming/full/finished)
- Automatic status calculation
- Available spots tracking

---

### 📝 Registration Management

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/registrations/{event_id}` | POST | Register for event | Authenticated |
| `/api/registrations/{event_id}` | DELETE | Cancel registration | Authenticated |
| `/api/registrations/my` | GET | Get user's registrations | Authenticated |

**Features:**
- Duplicate registration prevention
- Capacity limit enforcement
- Finished event registration blocked

---

### 📊 Statistics & Analytics

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/stats/dashboard` | GET | Admin dashboard statistics | Admin only |
| `/api/stats/my-stats` | GET | Current user's statistics | Authenticated |
| `/api/stats/events/{id}/stats` | GET | Event-specific statistics | Admin only |
| `/api/stats/leaderboard` | GET | Most active students ranking | Authenticated |

**Dashboard Stats Include:**
- Total users (students/admins breakdown)
- Total events (upcoming/finished)
- Registration trends (last 7 days)
- Most popular events (top 5)
- Daily registration chart data

**User Stats Include:**
- Total registrations
- Upcoming events count
- Attended events count
- Recent activity

**Event Stats Include:**
- Fill rate percentage
- Group distribution of participants
- Registration timeline

**Leaderboard:**
- Top 10 most active students
- Events attended count
- Group information

---

### 🔍 Advanced Search

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/search/events` | GET | Advanced event search | Authenticated |
| `/api/search/suggestions` | GET | Personalized event suggestions | Authenticated |

**Search Parameters:**
- `q` - Search query (title & description)
- `location` - Filter by location
- `date_from` - Filter from date (YYYY-MM-DD)
- `date_to` - Filter to date (YYYY-MM-DD)
- `has_spots` - Only events with available spots

**Suggestions:**
- Upcoming events user hasn't registered for
- Personalized based on registration history

---

### 📤 Data Export

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/export/events/csv` | GET | Export all events to CSV | Admin only |
| `/api/export/events/{id}/participants/csv` | GET | Export event participants to CSV | Admin only |
| `/api/export/users/csv` | GET | Export all users to CSV | Admin only |
| `/api/export/report` | GET | Comprehensive system report | Admin only |

**Report Includes:**
- User growth statistics
- Event statistics
- Registration trends
- Most active group insights

---

### ✅ Validation & Error Handling

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `204` - No Content (Delete)
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error

**Error Messages:**
- "Email already registered"
- "You are already registered"
- "No available spots"
- "Cannot register for finished event"
- "Event not found"
- "Admin access required"
- "Invalid secret key"

---

## 📁 Project Structure

```
Event_Project/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── event.py
│   │   │   └── registration.py
│   │   ├── schemas/         # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── event.py
│   │   │   └── registration.py
│   │   ├── services/        # Business logic
│   │   │   ├── auth.py
│   │   │   ├── user_service.py
│   │   │   ├── event_service.py
│   │   │   └── registration_service.py
│   │   ├── routers/         # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── events.py
│   │   │   ├── registrations.py
│   │   │   ├── stats.py      # Statistics endpoints
│   │   │   ├── search.py     # Search endpoints
│   │   │   └── export.py     # Export endpoints
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── middleware.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── AdminLogin.vue
│   │   │   ├── AdminRegister.vue
│   │   │   ├── Events.vue
│   │   │   ├── MyActivities.vue
│   │   │   └── Admin.vue
│   │   ├── stores/
│   │   ├── router/
│   │   └── api/
│   └── package.json
└── README.md
```

---

## 🛠️ How to Run

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000
```

**API Documentation:** http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

**Frontend:** http://localhost:5173

---

## 🌐 Frontend Pages

| URL | Description | Access |
|-----|-------------|--------|
| `/login` | Student login | Public |
| `/register` | Student registration | Public |
| `/admin/login` | Admin login | Public |
| `/admin/register` | Admin registration | Public |
| `/` | Events list | Students |
| `/my-activities` | User's registrations | Students |
| `/admin` | Admin panel | Admins |

---

## 🔑 Test Credentials

**Admin Secret Key:** `111111`

---

## 📝 API Examples (curl)

### Register Student
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@test.com","password":"123456","full_name":"John Doe","group":"1F1"}'
```

### Register Admin
```bash
curl -X POST http://localhost:8000/api/auth/admin/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"123456","full_name":"Admin","secret_key":"111111"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@test.com","password":"123456"}'
```

### Get Events
```bash
curl -X GET "http://localhost:8000/api/events/?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Search Events
```bash
curl -X GET "http://localhost:8000/api/search/events?q=chess&has_spots=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Dashboard Stats (Admin)
```bash
curl -X GET http://localhost:8000/api/stats/dashboard \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### Get Leaderboard
```bash
curl -X GET http://localhost:8000/api/stats/leaderboard \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Export Events CSV (Admin)
```bash
curl -X GET http://localhost:8000/api/export/events/csv \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -o events.csv
```

### Get System Report (Admin)
```bash
curl -X GET http://localhost:8000/api/export/report \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## 🗃️ Database Schema

### Users
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| email | VARCHAR(255) | Unique email |
| hashed_password | VARCHAR(255) | Bcrypt hash |
| full_name | VARCHAR(255) | User's name |
| group | VARCHAR(50) | Student group (e.g., 1F1) |
| role | ENUM | student / admin |
| created_at | DATETIME | Registration date |

### Events
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| title | VARCHAR(255) | Event title |
| description | TEXT | Event description |
| date | DATETIME | Event date/time |
| location | VARCHAR(255) | Room/location |
| max_participants | INTEGER | Capacity limit |
| created_by | INTEGER | FK → users |
| created_at | DATETIME | Creation date |

### Registrations
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | FK → users |
| event_id | INTEGER | FK → events |
| registered_at | DATETIME | Registration date |

**Constraints:** UNIQUE(user_id, event_id)

---

## ✅ Evaluation Criteria Met

| Criteria | Implementation |
|----------|---------------|
| **Auth + Role system** | JWT, Student/Admin roles, secret key for admin |
| **CRUD + Database relations** | Full CRUD, FK constraints, unique constraints |
| **API quality** | Validation, pagination, filtering, proper errors |
| **Advanced features** | Statistics, search, export, leaderboard |
| **Mini UI functionality** | Vue.js SPA with all features |
| **Git + README + Deployment** | Complete documentation |

---

## 📊 Total API Endpoints: 22

| Category | Count |
|----------|-------|
| Authentication | 3 |
| Users | 3 |
| Events | 6 |
| Registrations | 3 |
| Statistics | 4 |
| Search | 2 |
| Export | 4 |

---

## 👨‍💻 Author

JIHC Student Project - Full-Stack Web Technologies Final Exam
