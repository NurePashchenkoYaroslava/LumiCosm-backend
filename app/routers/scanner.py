from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import schemas, database, crud 

router = APIRouter(prefix="/scan", tags=["Client Scanner"])

@router.get("/{qr_code}", response_model=schemas.ScanResponse)
def scan_product(qr_code: str, user_id: int, db: Session = Depends(database.get_db)):
    batch = crud.get_batch_by_qr(db, qr_code)
    if not batch:
        raise HTTPException(status_code=404, detail="QR-код не знайдено") 
    today = date.today()
    calculated_status = "Valid"
    if batch.status == "disposed":
        calculated_status = "Disposed (Списано)"
    elif batch.ExpirationDate < today:
        calculated_status = "Expired (Прострочено)"
    if calculated_status != "Valid":
        warning_msg = (
            f"УВАГА! Клієнт (ID: {user_id}) просканував проблемний товар!\n"
            f"Товар: {batch.product.name} (Бренд: {batch.product.brand})\n"
            f"Партія ID: {batch.BatchID}\n"
            f"Причина: {calculated_status}"
        )
        crud.send_notification(user_email="manager@store.com", message=warning_msg)


    scan_entry = crud.create_scan_entry(db, user_id, batch.BatchID)
    
    return schemas.ScanResponse(
        product_name=batch.product.name,
        brand=batch.product.brand,
        expiration_date=batch.ExpirationDate,
        status_calculated=calculated_status,
        certificate_url=batch.Certificate,
        scan_time=scan_entry.ScanTime
    )

@router.post("/report_problem")
def report_problem(complaint: schemas.ComplaintCreate, user_id: int, db: Session = Depends(database.get_db)):
    crud.create_complaint(db, complaint, user_id)
    return {"message": "Скаргу відправлено менеджеру"}

@router.delete("/me/{user_id}")
def delete_my_account(user_id: int, db: Session = Depends(database.get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Your account has been deleted"}