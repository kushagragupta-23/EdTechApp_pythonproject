from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.utils import get_or_404, paginate

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("", response_model=schemas.PaginatedResponse[schemas.PaymentResponse])
def get_payments(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    return paginate(db, db.query(models.Payment), skip, limit)

@router.post("", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.User, payment.student_id)
    get_or_404(db, models.Course, payment.course_id)
    
    db_payment = db.query(models.Payment).filter(models.Payment.transaction_id == payment.transaction_id).first()
    if db_payment:
        raise HTTPException(status_code=400, detail="Transaction ID already recorded")
        
    new_payment = models.Payment(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.delete("/{payment_id}", response_model=dict)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = get_or_404(db, models.Payment, payment_id)
    db.delete(payment)
    db.commit()
    return {"detail": "Payment deleted"}
