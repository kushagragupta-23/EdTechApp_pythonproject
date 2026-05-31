from datetime import datetime
from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, EmailStr, Field

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int

# --- Users ---
class UserBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: EmailStr
    role: str = "student"
    age: Optional[int] = None
    gender: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

# --- Courses ---
class CourseBase(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    duration: Optional[str] = None
    prerequisites: Optional[str] = None
    instructor_id: Optional[int] = None
    video_link: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    is_active: bool

    model_config = {"from_attributes": True}

# --- Enrollments ---
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    payment_id: Optional[int] = None

class EnrollmentResponse(EnrollmentCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

# --- Payments ---
class PaymentCreate(BaseModel):
    student_id: int
    course_id: int
    transaction_id: str

class PaymentResponse(PaymentCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

# --- Reviews ---
class ReviewCreate(BaseModel):
    student_id: int
    course_id: int
    description: str

class ReviewResponse(ReviewCreate):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

# --- Certifications ---
class CertificationCreate(BaseModel):
    student_id: int
    course_id: int
    certificate_url: Optional[str] = None

class CertificationResponse(CertificationCreate):
    id: int
    issued_date: datetime

    model_config = {"from_attributes": True}

# --- Assignments ---
class AssignmentCreate(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[float] = None

class AssignmentResponse(AssignmentCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

# --- Submissions ---
class SubmissionCreate(BaseModel):
    assignment_id: int
    student_id: int
    content: str

class SubmissionResponse(SubmissionCreate):
    id: int
    score: Optional[float] = None
    submitted_at: datetime
    graded_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class SubmissionGrade(BaseModel):
    score: float

# --- Progress ---
class ProgressCreate(BaseModel):
    student_id: int
    course_id: int
    completion_percentage: float = 0.0
    status: str = "not_started"

class ProgressUpdate(BaseModel):
    completion_percentage: Optional[float] = None
    status: Optional[str] = None

class ProgressResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    completion_percentage: float
    last_accessed: datetime
    status: str

    model_config = {"from_attributes": True}

# --- Announcements ---
class AnnouncementCreate(BaseModel):
    course_id: int
    author_id: int
    title: str
    content: str

class AnnouncementResponse(AnnouncementCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
