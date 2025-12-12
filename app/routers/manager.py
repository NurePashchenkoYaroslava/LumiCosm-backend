from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, crud, models 
from datetime import date, timedelta

router = APIRouter(prefix="/manager", tags=["Manager Operations"])

@router.post("/create_batch")
def create_batch(batch_data: schemas.BatchCreate, store_id: int, db: Session = Depends(database.get_db)):
    new_batch = crud.create_batch(db=db, batch=batch_data, store_id=store_id)
    return {
        "message": "Партію створено успішно", 
        "batch_id": new_batch.BatchID, 
        "qr_code": new_batch.qr_code
    }

@router.post("/dispose/{batch_id}")
def dispose_batch(batch_id: int, db: Session = Depends(database.get_db)):
    result = crud.dispose_batch(db=db, batch_id=batch_id)
    if not result:
        raise HTTPException(status_code=404, detail="Партія не знайдена")
    return {"message": f"Batch {batch_id} marked as disposed"}

@router.get("/complaints", response_model=list[schemas.ComplaintResponse])
def get_complaints(store_id: int, db: Session = Depends(database.get_db)):
    complaints = crud.get_complaints_for_manager(db, store_id)   
    response = []
    for c in complaints:
        response.append({
            "ComplaintID": c.ComplaintID,
            "message": c.message,
            "status": c.status,
            "product_name": c.batch.product.name, 
            "user_email": c.user.email
        })
    return response

@router.delete("/batch/{batch_id}")
def delete_batch(batch_id: int, db: Session = Depends(database.get_db)):
    deleted = crud.delete_batch(db, batch_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"message": f"Batch {batch_id} deleted"}

@router.put("/batch/{batch_id}")
def update_batch_details(batch_id: int, updates: schemas.BatchUpdate, db: Session = Depends(database.get_db)):
    updated_batch = crud.update_batch(db, batch_id, updates)
    if not updated_batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"message": "Batch updated", "batch": updated_batch}

@router.get("/expiring_batches")
def get_expiring_batches(store_id: int, days_threshold: int = 7, db: Session = Depends(database.get_db)):
    today = date.today()
    threshold_date = today + timedelta(days=days_threshold)
    expiring_items = db.query(models.Batch).filter(
        models.Batch.StoreID == store_id,
        models.Batch.status == "active",
        (models.Batch.ExpirationDate < today) | (models.Batch.ExpirationDate <= threshold_date)
    ).all()
    
    result = []
    for batch in expiring_items:
        state = "Expired" if batch.ExpirationDate < today else "Expiring Soon"
        result.append({
            "BatchID": batch.BatchID,
            "Product": batch.product.name,
            "ExpirationDate": batch.ExpirationDate,
            "Status": state
        })
        
    return result