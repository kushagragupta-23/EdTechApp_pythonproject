from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.EnrollmentResponse])
def get_enrollments(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    return paginate(db, db.query(models.Enrollment), skip, limit)

@router.post("", response_model=schemas.EnrollmentResponse)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # Validate existence
    get_or_404(db, models.User, enrollment.student_id)
    get_or_404(db, models.Course, enrollment.course_id)
    if enrollment.payment_id:
        get_or_404(db, models.Payment, enrollment.payment_id)
        
    new_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

@router.delete("/{enrollment_id}", response_model=dict)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    en = get_or_404(db, models.Enrollment, enrollment_id)
    db.delete(en)
    db.commit()
    return {"detail": "Enrollment deleted"}
