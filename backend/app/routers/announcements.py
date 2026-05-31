from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/announcements", tags=["Announcements"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.AnnouncementResponse])
def get_announcements(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), course_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Announcement)
    if course_id:
        query = query.filter(models.Announcement.course_id == course_id)
    return paginate(db, query, skip, limit)

@router.post("", response_model=schemas.AnnouncementResponse)
def create_announcement(announcement: schemas.AnnouncementCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.Course, announcement.course_id)
    get_or_404(db, models.User, announcement.author_id)
    
    new_announcement = models.Announcement(**announcement.model_dump())
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

@router.delete("/{announcement_id}", response_model=dict)
def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    ann = get_or_404(db, models.Announcement, announcement_id)
    db.delete(ann)
    db.commit()
    return {"detail": "Announcement deleted"}
