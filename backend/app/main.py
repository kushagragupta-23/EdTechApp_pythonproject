import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import (
    users, courses, enrollments, payments,
    reviews, certifications, assignments,
    progress, announcements, ai
)

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="Advanced backend for EduVerse"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request ID & Logging Middleware
@app.middleware("http")
async def add_request_id_and_process_time(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Health check
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "database_url": settings.DATABASE_URL
    }

# Include all routers under API prefix
api_router = FastAPI()
api_router.include_router(users.router)
api_router.include_router(courses.router)
api_router.include_router(enrollments.router)
api_router.include_router(payments.router)
api_router.include_router(reviews.router)
api_router.include_router(certifications.router)
api_router.include_router(assignments.router)
api_router.include_router(progress.router)
api_router.include_router(announcements.router)
api_router.include_router(ai.router)

app.mount("/api/v1", api_router)

# For backward compatibility during migration, alias to root:
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(payments.router)
app.include_router(reviews.router)
app.include_router(certifications.router)
app.include_router(assignments.router)
app.include_router(progress.router)
app.include_router(announcements.router)
app.include_router(ai.router)
