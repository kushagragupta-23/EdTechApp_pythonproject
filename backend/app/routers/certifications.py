from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/certifications", tags=["Certifications"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.CertificationResponse])
def get_certifications(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    return paginate(db, db.query(models.Certification), skip, limit)

@router.post("", response_model=schemas.CertificationResponse)
def create_certification(cert: schemas.CertificationCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.User, cert.student_id)
    get_or_404(db, models.Course, cert.course_id)
    
    new_cert = models.Certification(**cert.model_dump())
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return new_cert

@router.delete("/{cert_id}", response_model=dict)
def delete_certification(cert_id: int, db: Session = Depends(get_db)):
    cert = get_or_404(db, models.Certification, cert_id)
    db.delete(cert)
    db.commit()
    return {"detail": "Certification deleted"}
