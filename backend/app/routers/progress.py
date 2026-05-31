from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.ProgressResponse])
def get_progress(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), student_id: int = None, course_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Progress)
    if student_id:
        query = query.filter(models.Progress.student_id == student_id)
    if course_id:
        query = query.filter(models.Progress.course_id == course_id)
    return paginate(db, query, skip, limit)

@router.post("", response_model=schemas.ProgressResponse)
def create_progress(progress: schemas.ProgressCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.User, progress.student_id)
    get_or_404(db, models.Course, progress.course_id)
    
    db_prog = db.query(models.Progress).filter(
        models.Progress.student_id == progress.student_id,
        models.Progress.course_id == progress.course_id
    ).first()
    
    if db_prog:
        raise HTTPException(status_code=400, detail="Progress record already exists")
        
    new_prog = models.Progress(**progress.model_dump())
    db.add(new_prog)
    db.commit()
    db.refresh(new_prog)
    return new_prog

@router.put("/{progress_id}", response_model=schemas.ProgressResponse)
def update_progress(progress_id: int, progress: schemas.ProgressUpdate, db: Session = Depends(get_db)):
    prog = get_or_404(db, models.Progress, progress_id)
    if progress.completion_percentage is not None:
        prog.completion_percentage = progress.completion_percentage
    if progress.status is not None:
        prog.status = progress.status
    prog.last_accessed = datetime.utcnow()
    db.commit()
    db.refresh(prog)
    return prog
