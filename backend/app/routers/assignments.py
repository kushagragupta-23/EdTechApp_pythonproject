from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.AssignmentResponse])
def get_assignments(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), course_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Assignment)
    if course_id:
        query = query.filter(models.Assignment.course_id == course_id)
    return paginate(db, query, skip, limit)

@router.post("", response_model=schemas.AssignmentResponse)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.Course, assignment.course_id)
    new_assignment = models.Assignment(**assignment.model_dump())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.delete("/{assignment_id}", response_model=dict)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = get_or_404(db, models.Assignment, assignment_id)
    db.delete(assignment)
    db.commit()
    return {"detail": "Assignment deleted"}

# --- Submissions ---
@router.post("/{assignment_id}/submissions", response_model=schemas.SubmissionResponse)
def submit_assignment(assignment_id: int, submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.Assignment, assignment_id)
    get_or_404(db, models.User, submission.student_id)
    
    new_sub = models.Submission(assignment_id=assignment_id, **submission.model_dump(exclude={"assignment_id"}))
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

@router.put("/{assignment_id}/submissions/{submission_id}/grade", response_model=schemas.SubmissionResponse)
def grade_submission(assignment_id: int, submission_id: int, grade: schemas.SubmissionGrade, db: Session = Depends(get_db)):
    sub = get_or_404(db, models.Submission, submission_id)
    sub.score = grade.score
    sub.graded_at = datetime.utcnow()
    db.commit()
    db.refresh(sub)
    return sub
