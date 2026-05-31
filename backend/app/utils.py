from typing import Type, TypeVar, Optional, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

T = TypeVar("T")

def get_or_404(db: Session, model: Type[T], obj_id: int) -> T:
    obj = db.query(model).filter(model.id == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} {obj_id} not found")
    return obj

def paginate(db: Session, query, skip: int, limit: int) -> dict:
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }
