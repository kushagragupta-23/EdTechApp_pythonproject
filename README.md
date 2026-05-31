# EduVerse — EdTech Platform

A full-stack e-learning platform built with **FastAPI** (Python) backend and a **vanilla HTML/CSS/JavaScript** frontend.

## 👥 Team

- **Kushagra Gupta**
- **Aishwarya Nevrekar**
- **Sampad Kar**
- **Niladri Ghosh**
- **Jayanth Vukkisa**

---

## 🚀 Features

| Section | Description |
|---|---|
| **Users** | Full CRUD for students, instructors, and admins with profile details (bio, age, gender, phone) |
| **Courses** | Course management with codes, categories, durations, prerequisites, video links, and instructor assignments |
| **Enrollments** | Student–course enrollment tracking linked to payments |
| **Payments** | Transaction recording with unique transaction IDs |
| **Reviews** | Student reviews and feedback for each course |
| **Certifications** | Certificate issuance for completed courses with certificate URLs |
| **Assignments** | Course assignments with descriptions, max scores, and due dates |
| **Progress** | Student progress tracking with completion percentage and status (not started / in progress / completed) |
| **Announcements** | Course announcements from instructors |
| **AI Tools** | Quiz generator, virtual teacher, research finder, student performance analysis |

## 🏗 Tech Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy 2.0, Pydantic v2, Uvicorn
- **Database**: SQLite (file-based, zero-config)
- **Frontend**: HTML5, CSS3 (custom design tokens, dark mode), Vanilla JavaScript
- **Fonts**: Inter (Google Fonts)
- **Icons**: Lucide Icons
- **Migrations**: Alembic

## 📁 Project Structure

```
EdTechApp_pythonproject/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # App settings (DB URL, version)
│   │   ├── database.py        # SQLAlchemy engine & session
│   │   ├── main.py            # FastAPI app with middleware & routers
│   │   ├── models.py          # SQLAlchemy ORM models (10 tables)
│   │   ├── schemas.py         # Pydantic request/response schemas
│   │   ├── utils.py           # Helper utilities (pagination, 404)
│   │   └── routers/           # Route handlers per entity
│   │       ├── users.py
│   │       ├── courses.py
│   │       ├── enrollments.py
│   │       ├── payments.py
│   │       ├── reviews.py
│   │       ├── certifications.py
│   │       ├── assignments.py
│   │       ├── progress.py
│   │       ├── announcements.py
│   │       └── ai.py
│   ├── alembic/               # Database migration scripts
│   ├── main.py                # Legacy monolithic backend (standalone)
│   ├── run.py                 # Entry point: `python run.py`
│   ├── seed_data.py           # Seed script to populate sample data
│   └── requirements.txt       # Python dependencies
├── frontend/
│   └── index.html             # Single-page application (66KB)
└── docs/
    ├── report.md              # Project report
    └── images/                # Architecture diagrams
```

## ⚡ Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Database Tables

```bash
python -c "from app.database import Base, engine; from app import models; Base.metadata.create_all(bind=engine)"
```

### 3. Start the Backend Server

```bash
python run.py --reload
```

The API will be available at **http://localhost:8000**
- API docs (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 4. Seed Sample Data (Optional)

```bash
python seed_data.py
```

This populates the database with **10 users**, **6 courses**, **20 enrollments**, **20 payments**, **15 reviews**, **13 assignments**, **20 progress entries**, **4 certifications**, and **11 announcements**.

### 5. Start the Frontend

```bash
cd frontend
python -m http.server 3000
```

Open **http://localhost:3000** in your browser.

## 📊 Sample Data Overview

### Users (10)
| Role | Count | Examples |
|---|---|---|
| Instructors | 3 | Dr. Priya Sharma (CS/ML), Prof. Rajesh Kumar (DBMS/Cloud), Dr. Ananya Patel (Math) |
| Students | 7 | Kushagra Gupta, Aishwarya Nevrekar, Sampad Kar, Niladri Ghosh, Kavya Iyer, Rohit Deshmukh, Aisha Khan |

### Courses (6)
| Code | Title | Category | Duration |
|---|---|---|---|
| CS201 | Data Structures & Algorithms | Computer Science | 16 weeks |
| CS301 | Database Management Systems | Computer Science | 14 weeks |
| MA201 | Linear Algebra for Engineers | Mathematics | 12 weeks |
| CS401 | Machine Learning Fundamentals | Artificial Intelligence | 16 weeks |
| CS202 | Web Development Full Stack | Web Development | 18 weeks |
| CS501 | Cloud Computing & DevOps | Cloud & Infrastructure | 14 weeks |

## 🔌 API Endpoints

All entity endpoints follow RESTful conventions:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/{entity}` | List all (paginated) |
| `POST` | `/api/v1/{entity}` | Create new |
| `GET` | `/api/v1/{entity}/{id}` | Get by ID |
| `DELETE` | `/api/v1/{entity}/{id}` | Delete by ID |

Entities: `users`, `courses`, `enrollments`, `payments`, `reviews`, `certifications`, `assignments`, `progress`, `announcements`

## 📄 License

This project is for academic/educational purposes.
