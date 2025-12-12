from sqlalchemy.orm import Session
from datetime import date
from . import models, schemas
import uuid
from . import security  

# Адмін
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password) 
    db_user = models.User(
        email=user.email,
        password=hashed_password, 
        FullName=user.FullName,
        role=user.role,
        StoreID=user.StoreID
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_store(db: Session, store: schemas.StoreCreate):
    db_store = models.Store(name=store.name, address=store.address, city=store.city)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_store(db: Session, store_id: int):
    store = db.query(models.Store).filter(models.Store.StoreID == store_id).first()
    if store:
        db.delete(store)
        db.commit()
    return store

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.ProductID == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def update_store_address(db: Session, store_id: int, new_address: str):
    store = db.query(models.Store).filter(models.Store.StoreID == store_id).first()
    if store:
        store.address = new_address
        db.commit()
        db.refresh(store)
    return store

def update_product(db: Session, product_id: int, updates: schemas.ProductUpdate):
    product = db.query(models.Product).filter(models.Product.ProductID == product_id).first()
    if not product:
        return None
    
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

def update_user(db: Session, user_id: int, updates: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if not user:
        return None
    
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
        
    db.commit()
    db.refresh(user)
    return user
# Менеджер
def create_batch(db: Session, batch: schemas.BatchCreate, store_id: int):
    generated_qr = str(uuid.uuid4())
    
    db_batch = models.Batch(
        StoreID=store_id,
        ProductID=batch.ProductID,
        qr_code=generated_qr,
        ManufactureDate=batch.ManufactureDate,
        ExpirationDate=batch.ExpirationDate,
        Quantity=batch.Quantity,
        Certificate=batch.Certificate,
        status="active"
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

def dispose_batch(db: Session, batch_id: int):
    batch = db.query(models.Batch).filter(models.Batch.BatchID == batch_id).first()
    if batch:
        batch.status = "disposed"
        db.commit()
        db.refresh(batch)
    return batch

def get_complaints_for_manager(db: Session, store_id: int):
    return db.query(models.Complaint)\
        .join(models.Batch)\
        .filter(models.Batch.StoreID == store_id)\
        .filter(models.Complaint.status == "new")\
        .all()

def delete_batch(db: Session, batch_id: int):
    batch = db.query(models.Batch).filter(models.Batch.BatchID == batch_id).first()
    if batch:
        db.delete(batch)
        db.commit()
    return batch

def update_batch(db: Session, batch_id: int, updates: schemas.BatchUpdate):
    batch = db.query(models.Batch).filter(models.Batch.BatchID == batch_id).first()
    if not batch:
        return None
    
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(batch, key, value)
        
    db.commit()
    db.refresh(batch)
    return batch

# Клієнт
def get_batch_by_qr(db: Session, qr_code: str):
    return db.query(models.Batch).filter(models.Batch.qr_code == qr_code).first()

def create_scan_entry(db: Session, user_id: int, batch_id: int):
    db_scan = models.ScanHistory(UserID=user_id, BatchID=batch_id)
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan

def get_user_history(db: Session, user_id: int):
    return db.query(models.ScanHistory).filter(models.ScanHistory.UserID == user_id).all()

def create_complaint(db: Session, complaint: schemas.ComplaintCreate, user_id: int):
    db_complaint = models.Complaint(
        UserID=user_id,
        BatchID=complaint.BatchID,
        message=complaint.message
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

def send_notification(user_email: str, message: str):
    print("\n" + "="*50)
    print(f" >>> [MOCK EMAIL SERVICE] SENDING ALERT...")
    print(f" To:      {user_email}")
    print(f" Subject: !!!ПОПЕРЕДЖЕННЯ ПРО ЯКІСТЬ ПРОДУКЦІЇ")
    print(f" Body:    \n{message}")
    print("="*50 + "\n")