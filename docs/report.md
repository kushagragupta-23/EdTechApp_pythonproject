# EdTech Platform Design and Implementation

This document presents a comprehensive design for an AI‑enabled e‑learning platform.  It covers the **Logical Data Design (LDD)**, **High‑Level Design (HDD)** and **System Design Diagram (SDD)**, followed by a brief description of the implemented backend and a simple browser‑based frontend.

## Team Members

* **Kushagra Gupta**
* **Aishwarya Nevrekar**
* **Sampad Kar**
* **Niladri Ghosh**
* **Jayanth Vukkisa**

## Overview and Requirements

The platform is intended to support students, instructors and administrative staff.  Key capabilities include:

* **Student experience:** Students need a profile, the ability to browse available courses, enrol, track their progress and interact with teachers and peers.  The Hygraph architecture guidelines emphasise that a student interface should allow students to create a school profile, view available courses and track learning progress【242159687018151†L170-L203】.
* **Teacher experience:** Teachers must manage course content, schedules and enrolled students, and they should be able to create and mark exams【242159687018151†L205-L229】.
* **Administrator experience:** Administrators approve courses and enrolments, manage departments and promote students.  They also need to oversee the e‑learning process and block inappropriate content【242159687018151†L233-L270】.

In addition to typical course management, the system should provide AI‑driven features such as performance tracking, question answering, interactive teaching with virtual AI tutors, customised quizzes and access to recent research findings.

## Logical Data Design (LDD)

The logical data design identifies the core entities and their relationships.  The table below summarises the main entities and attributes.

| Entity | Primary Attributes | Relationships |
|---|---|---|
| **User** (roles: student/instructor/admin) | `id`, `name`, `phone`, `email`, `address`, `age`, `gender`, `bio`, `photo`, `is_active`, `role`, `created_at`, `updated_at` | Instructors own many courses; students have many enrolments, payments, reviews and certifications |
| **Course** | `id`, `name`, `duration`, `title`, `description`, `category`, `prerequisites`, `video_link`, `is_active`, `created_at`, `updated_at`, `instructor_id` | Has many enrolments, payments, reviews, certifications; taught by one instructor |
| **Enrollment** | `id`, `student_id`, `course_id`, `payment_id`, `created_at`, `updated_at` | Links students to courses; may reference a payment |
| **Payment** | `id`, `student_id`, `course_id`, `transaction_id`, `created_at`, `updated_at` | Associated with a student and a course; optionally linked back to an enrollment |
| **Review** | `id`, `student_id`, `course_id`, `description`, `is_active`, `created_at`, `updated_at` | Student‑authored feedback on courses |
| **Certification** | `id`, `student_id`, `course_id`, `certificate_url`, `issued_date`, `created_at` | Issued upon course completion |

The relationships are illustrated in the LDD diagram below.  Directed edges label the foreign‑key fields.  Students enrol in courses and may make payments.  Reviews and certifications connect students and courses.  Courses may specify an instructor via the `instructor_id` field.

![Logical Data Design]({{file:file-NJxYVL1NiUVkLm7S7WxdvM}})

## High‑Level Design (HDD)

At a high level, the system consists of a web‑based frontend communicating with a FastAPI backend via HTTP/REST.  The backend persists data using an SQL database (SQLite by default) and communicates with AI services for tasks such as answering questions and generating customised quizzes.  This modular, API‑first approach aligns with the **MACH** (Microservices, API‑first, Cloud‑native, Headless) architecture recommended for modern e‑learning platforms【242159687018151†L136-L143】.

![High‑Level Design]({{file:file-3QqYvdT2Vnifac68Fx9DvE}})

Components:

* **Frontend (Web UI):** A simple browser interface built with HTML and JavaScript.  It allows users to register, create courses and view available courses.  Additional pages can be added for enrolments, payments and AI interactions.
* **FastAPI Backend:** Implements CRUD operations for all entities, handles authentication/authorisation (not fully implemented in this example) and exposes endpoints for AI‑driven features such as performance tracking, question answering and quiz generation.
* **Database:** Uses SQLAlchemy with SQLite; can be switched to PostgreSQL or another database without code changes.
* **AI Services:** External or internal services that provide language‑model responses, quiz generation and retrieval of recent research.  These are stubbed out in the initial implementation.

## System Design Diagram (SDD)

The system design breaks the backend into several services.  Each service contains business logic for a particular domain and interacts with the database through an ORM (SQLAlchemy).  The **AI Module** acts as a bridge to AI models and external research APIs.

![System Design Diagram]({{file:file-GW8vF875ehgyCnm1wwXp2N}})

* **User Service:** Manages user accounts (students, instructors, admins).
* **Course Service:** Handles course creation, updates and deletion; associates instructors.
* **Enrollment Service:** Manages student enrolments and references payments.
* **Payment Service:** Records payments linked to students and courses.
* **Review Service:** Allows students to submit reviews for courses.
* **Certification Service:** Issues certificates when students complete courses.
* **AI Module:** Provides endpoints for performance tracking, question answering, virtual teaching, quiz generation and retrieving research insights.

## Backend Implementation

The backend is implemented in Python using FastAPI and SQLAlchemy.  A database session is provided per request via a dependency, ensuring proper cleanup.  Each entity has corresponding Pydantic models for input validation and response serialization.  CRUD endpoints are defined for all core entities (`/users`, `/courses`, `/enrollments`, `/payments`, `/reviews`, `/certifications`).  Additional endpoints include:

* `GET /performance/{student_id}`: Returns a placeholder performance report.
* `GET /answer`: Answers arbitrary questions using a stubbed AI response.
* `POST /quiz/{course_id}`: Generates a simple quiz for a course.
* `GET /virtual_teacher/{course_id}/ask`: Simulates a virtual AI teacher for a course.
* `GET /research`: Returns mock research findings for a given domain.

The application uses SQLite as a default database but can be configured via the ``DATABASE_URL`` environment variable.  To run the server locally:

```bash
pip install fastapi uvicorn sqlalchemy pydantic
uvicorn main:app --reload
```

FastAPI automatically generates interactive API documentation at `/docs`.

## Frontend Implementation

A simple HTML/JavaScript frontend demonstrates how to interact with the API.  It provides forms for creating users and courses and a table listing available courses.  The code can be extended to cover enrolments, payments and AI features.  To use it locally, start the FastAPI server, then open ``edtech_app/frontend/index.html`` in your browser.  Make sure the API is running at ``http://localhost:8000`` or update the ``API_BASE`` constant in the JavaScript.

## Future Enhancements

This architecture serves as a foundation.  Further enhancements might include:

* **Authentication and Authorisation:** Implement JWT‑based authentication with role‑based permissions to secure endpoints.
* **Asynchronous Processing:** Use asynchronous ORM (e.g., SQLModel or async SQLAlchemy) to improve scalability.
* **Real AI Integration:** Connect the AI Module to actual language models or retrieval‑augmented generation systems to answer questions and generate quizzes.
* **User Interface:** Build a richer frontend using modern frameworks (React, Vue) with role‑specific dashboards for students, teachers and administrators, reflecting the interface guidelines highlighted by Hygraph【242159687018151†L170-L203】【242159687018151†L205-L229】【242159687018151†L233-L270】.
* **Analytics:** Develop a robust performance tracking service drawing on course completion rates, quiz scores and time‑spent metrics.

This design demonstrates how to combine a clean data model, modular architecture and AI‑powered features to create an engaging e‑learning experience.