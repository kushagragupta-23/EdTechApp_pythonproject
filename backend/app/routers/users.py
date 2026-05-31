from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    q: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.User)
    if q:
        query = query.filter(models.User.name.ilike(f"%{q}%") | models.User.email.ilike(f"%{q}%"))
    if role:
        query = query.filter(models.User.role == role)
    return paginate(db, query, skip, limit)

@router.post("", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_or_404(db, models.User, user_id)
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
