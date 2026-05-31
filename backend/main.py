"""
EdTech Platform Backend
=======================

FastAPI + SQLAlchemy backend for the EdTech Platform.
Serves at http://localhost:8000 with CORS enabled for the frontend.

Run:
    uvicorn main:app --reload
"""

import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import (Column, DateTime, Integer, String, Boolean,
                        ForeignKey, create_engine)
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase, Session

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./edtech.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency to provide a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Database models
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    courses = relationship("Course", back_populates="instructor",
                           cascade="all, delete-orphan", foreign_keys="Course.instructor_id")
    enrollments = relationship("Enrollment", back_populates="student")
    payments = relationship("Payment", back_populates="student")
    reviews = relationship("Review", back_populates="student")
    certifications = relationship("Certification", back_populates="student")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration = Column(String, nullable=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    prerequisites = Column(String, nullable=True)
    video_link = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    instructor = relationship("User", back_populates="courses", foreign_keys=[instructor_id])
    enrollments = relationship("Enrollment", back_populates="course")
    payments = relationship("Payment", back_populates="course")
    reviews = relationship("Review", back_populates="course")
    certifications = relationship("Certification", back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    payment = relationship("Payment", back_populates="enrollment", uselist=False)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    transaction_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", back_populates="payments")
    course = relationship("Course", back_populates="payments")
    enrollment = relationship("Enrollment", back_populates="payment", uselist=False)


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("User", back_populates="reviews")
    course = relationship("Course", back_populates="reviews")


class Certification(Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    certificate_url = Column(String, nullable=True)
    issued_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", back_populates="certifications")
    course = relationship("Course", back_populates="certifications")


Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# Pydantic schemas  (Pydantic v2: model_config instead of class Config)
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    photo: Optional[str] = None
    role: str = Field(..., description="'student', 'instructor', or 'admin'")


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    photo: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


class UserOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    phone: Optional[str] = None
    email: EmailStr
    address: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    photo: Optional[str] = None
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime


class CourseCreate(BaseModel):
    name: str
    duration: Optional[str] = None
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    prerequisites: Optional[str] = None
    video_link: Optional[str] = None
    is_active: Optional[bool] = True
    instructor_id: Optional[int] = None


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    duration: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    prerequisites: Optional[str] = None
    video_link: Optional[str] = None
    is_active: Optional[bool] = None
    instructor_id: Optional[int] = None


class CourseOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    duration: Optional[str] = None
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    prerequisites: Optional[str] = None
    video_link: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    instructor_id: Optional[int] = None


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    payment_id: Optional[int] = None


class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    payment_id: Optional[int] = None


class EnrollmentOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    student_id: int
    course_id: int
    payment_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class PaymentCreate(BaseModel):
    student_id: int
    course_id: int
    transaction_id: str


class PaymentUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    transaction_id: Optional[str] = None


class PaymentOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    student_id: int
    course_id: int
    transaction_id: str
    created_at: datetime
    updated_at: datetime


class ReviewCreate(BaseModel):
    student_id: int
    course_id: int
    description: str
    is_active: Optional[bool] = True


class ReviewUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ReviewOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    student_id: int
    course_id: int
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CertificationCreate(BaseModel):
    student_id: int
    course_id: int
    certificate_url: Optional[str] = None
    issued_date: Optional[datetime] = None


class CertificationUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    certificate_url: Optional[str] = None
    issued_date: Optional[datetime] = None


class CertificationOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    student_id: int
    course_id: int
    certificate_url: Optional[str] = None
    issued_date: Optional[datetime] = None
    created_at: datetime


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="EdTech Platform API",
    description="API for an e-learning platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_user_or_404(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_course_or_404(db: Session, course_id: int) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def get_enrollment_or_404(db: Session, enrollment_id: int) -> Enrollment:
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


def get_payment_or_404(db: Session, payment_id: int) -> Payment:
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def get_review_or_404(db: Session, review_id: int) -> Review:
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


def get_certification_or_404(db: Session, certification_id: int) -> Certification:
    cert = db.query(Certification).filter(Certification.id == certification_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    return cert


# ---------------------------------------------------------------------------
# User endpoints
# ---------------------------------------------------------------------------

@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", response_model=List[UserOut])
def list_users(role: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.all()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(db, user_id)


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = get_user_or_404(db, user_id)
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(db, user_id)
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


# ---------------------------------------------------------------------------
# Course endpoints
# ---------------------------------------------------------------------------

@app.post("/courses", response_model=CourseOut)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.get("/courses", response_model=List[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return get_course_or_404(db, course_id)


@app.put("/courses/{course_id}", response_model=CourseOut)
def update_course(course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)):
    course = get_course_or_404(db, course_id)
    for field, value in course_update.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/courses/{course_id}", response_model=dict)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = get_course_or_404(db, course_id)
    db.delete(course)
    db.commit()
    return {"detail": "Course deleted"}


# ---------------------------------------------------------------------------
# Enrollment endpoints
# ---------------------------------------------------------------------------

@app.post("/enrollments", response_model=EnrollmentOut)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    get_user_or_404(db, enrollment.student_id)
    get_course_or_404(db, enrollment.course_id)
    new_enrollment = Enrollment(**enrollment.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment


@app.get("/enrollments", response_model=List[EnrollmentOut])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()


@app.get("/enrollments/{enrollment_id}", response_model=EnrollmentOut)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    return get_enrollment_or_404(db, enrollment_id)


@app.put("/enrollments/{enrollment_id}", response_model=EnrollmentOut)
def update_enrollment(enrollment_id: int, enrollment_update: EnrollmentUpdate, db: Session = Depends(get_db)):
    enrollment = get_enrollment_or_404(db, enrollment_id)
    for field, value in enrollment_update.model_dump(exclude_unset=True).items():
        setattr(enrollment, field, value)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@app.delete("/enrollments/{enrollment_id}", response_model=dict)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = get_enrollment_or_404(db, enrollment_id)
    db.delete(enrollment)
    db.commit()
    return {"detail": "Enrollment deleted"}


# ---------------------------------------------------------------------------
# Payment endpoints
# ---------------------------------------------------------------------------

@app.post("/payments", response_model=PaymentOut)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    get_user_or_404(db, payment.student_id)
    get_course_or_404(db, payment.course_id)
    new_payment = Payment(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@app.get("/payments", response_model=List[PaymentOut])
def list_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


@app.get("/payments/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return get_payment_or_404(db, payment_id)


@app.put("/payments/{payment_id}", response_model=PaymentOut)
def update_payment(payment_id: int, payment_update: PaymentUpdate, db: Session = Depends(get_db)):
    payment = get_payment_or_404(db, payment_id)
    for field, value in payment_update.model_dump(exclude_unset=True).items():
        setattr(payment, field, value)
    db.commit()
    db.refresh(payment)
    return payment


@app.delete("/payments/{payment_id}", response_model=dict)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = get_payment_or_404(db, payment_id)
    db.delete(payment)
    db.commit()
    return {"detail": "Payment deleted"}


# ---------------------------------------------------------------------------
# Review endpoints
# ---------------------------------------------------------------------------

@app.post("/reviews", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    get_user_or_404(db, review.student_id)
    get_course_or_404(db, review.course_id)
    new_review = Review(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@app.get("/reviews", response_model=List[ReviewOut])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@app.get("/reviews/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    return get_review_or_404(db, review_id)


@app.put("/reviews/{review_id}", response_model=ReviewOut)
def update_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db)):
    review = get_review_or_404(db, review_id)
    for field, value in review_update.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return review


@app.delete("/reviews/{review_id}", response_model=dict)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = get_review_or_404(db, review_id)
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted"}


# ---------------------------------------------------------------------------
# Certification endpoints
# ---------------------------------------------------------------------------

@app.post("/certifications", response_model=CertificationOut)
def create_certification(cert: CertificationCreate, db: Session = Depends(get_db)):
    get_user_or_404(db, cert.student_id)
    get_course_or_404(db, cert.course_id)
    new_cert = Certification(**cert.model_dump())
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return new_cert


@app.get("/certifications", response_model=List[CertificationOut])
def list_certifications(db: Session = Depends(get_db)):
    return db.query(Certification).all()


@app.get("/certifications/{cert_id}", response_model=CertificationOut)
def get_certification(cert_id: int, db: Session = Depends(get_db)):
    return get_certification_or_404(db, cert_id)


@app.put("/certifications/{cert_id}", response_model=CertificationOut)
def update_certification(cert_id: int, cert_update: CertificationUpdate, db: Session = Depends(get_db)):
    cert = get_certification_or_404(db, cert_id)
    for field, value in cert_update.model_dump(exclude_unset=True).items():
        setattr(cert, field, value)
    db.commit()
    db.refresh(cert)
    return cert


@app.delete("/certifications/{cert_id}", response_model=dict)
def delete_certification(cert_id: int, db: Session = Depends(get_db)):
    cert = get_certification_or_404(db, cert_id)
    db.delete(cert)
    db.commit()
    return {"detail": "Certification deleted"}


# ---------------------------------------------------------------------------
# AI feature endpoints (placeholders)
# ---------------------------------------------------------------------------

@app.get("/performance/{student_id}", response_model=dict)
def track_performance(student_id: int, db: Session = Depends(get_db)):
    """Return a placeholder performance report for the given student."""
    get_user_or_404(db, student_id)
    return {
        "student_id": student_id,
        "performance_score": 0.85,
        "strengths": ["Mathematics", "Physics"],
        "weaknesses": ["Chemistry"],
        "recommendations": ["Spend more time on assignments", "Participate in discussions"]
    }


@app.get("/answer", response_model=dict)
def answer_question(question: str = Query(..., description="The question to answer")):
    """Answer a user question using a stub AI logic."""
    return {
        "question": question,
        "answer": f"This is a placeholder answer for: {question}"
    }


@app.post("/quiz/{course_id}", response_model=dict)
def generate_quiz(course_id: int, num_questions: int = 5, db: Session = Depends(get_db)):
    """Generate a simple quiz for the given course."""
    course = get_course_or_404(db, course_id)
    questions = []
    for i in range(1, num_questions + 1):
        questions.append({
            "question": f"Question {i} for course '{course.title}'",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A"
        })
    return {"course_id": course_id, "questions": questions}


@app.get("/virtual_teacher/{course_id}/ask", response_model=dict)
def ask_virtual_teacher(course_id: int, question: str, db: Session = Depends(get_db)):
    """Simulate a virtual AI teacher answering a question for a course."""
    course = get_course_or_404(db, course_id)
    return {
        "course_id": course_id,
        "question": question,
        "answer": f"This is a virtual teacher's answer to '{question}' for course '{course.title}'."
    }


@app.get("/research", response_model=dict)
def get_research(domain: str = Query(..., description="Domain to search for new research")):
    """Placeholder endpoint returning recent research topics."""
    return {
        "domain": domain,
        "findings": [
            f"Latest research in {domain} 1",
            f"Latest research in {domain} 2",
            f"Latest research in {domain} 3"
        ]
    }