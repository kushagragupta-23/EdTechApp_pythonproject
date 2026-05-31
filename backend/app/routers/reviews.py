from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.ReviewResponse])
def get_reviews(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    return paginate(db, db.query(models.Review), skip, limit)

@router.post("", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.User, review.student_id)
    get_or_404(db, models.Course, review.course_id)
    
    new_review = models.Review(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.delete("/{review_id}", response_model=dict)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = get_or_404(db, models.Review, review_id)
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted"}
