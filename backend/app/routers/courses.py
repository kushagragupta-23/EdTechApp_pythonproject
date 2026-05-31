from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.CourseResponse])
def get_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    q: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Course)
    if q:
        query = query.filter(models.Course.name.ilike(f"%{q}%") | models.Course.title.ilike(f"%{q}%"))
    if category:
        query = query.filter(models.Course.category == category)
    return paginate(db, query, skip, limit)

@router.post("", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.name == course.name).first()
    if db_course:
        raise HTTPException(status_code=400, detail="Course code already exists")
    new_course = models.Course(**course.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.delete("/{course_id}", response_model=dict)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = get_or_404(db, models.Course, course_id)
    db.delete(course)
    db.commit()
    return {"detail": "Course deleted"}
