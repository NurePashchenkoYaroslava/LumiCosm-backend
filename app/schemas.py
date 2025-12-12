from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime

# --- 1. БАЗОВІ СХЕМИ ---
class StoreCreate(BaseModel):
    name: str
    address: str
    city: str

class StoreResponse(StoreCreate):
    StoreID: int
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name: str
    brand: str
    category: str
    description: str

class ProductResponse(ProductCreate):   # <--- Перевірте наявність цього класу
    ProductID: int
    model_config = ConfigDict(from_attributes=True)

# --- 2. СХЕМИ ДЛЯ ЮЗЕРІВ (AUTH) ---
class UserCreate(BaseModel):
    email: str
    password: str
    FullName: str          # Виправлено з full_name, щоб збігалося з models.py
    role: str = "client"
    StoreID: Optional[int] = None # Виправлено з store_id

class UserResponse(BaseModel):
    UserID: int
    email: str
    FullName: str
    role: str
    StoreID: Optional[int] = None 
    
    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: str
    password: str

# --- 3. СХЕМИ ДЛЯ МЕНЕДЖЕРА (ПАРТІЇ) ---
class BatchCreate(BaseModel):
    ProductID: int
    Quantity: int
    ManufactureDate: date
    ExpirationDate: date
    Certificate: Optional[str] = None

class BatchResponse(BatchCreate):
    BatchID: int
    StoreID: int
    qr_code: Optional[str] = None
    status: str
    
    model_config = ConfigDict(from_attributes=True)

# --- 4. СХЕМИ ДЛЯ КЛІЄНТА (СКАНУВАННЯ) ---
class ScanResponse(BaseModel):
    product_name: str
    brand: str
    expiration_date: date
    status_calculated: str
    certificate_url: Optional[str]
    scan_time: datetime

    model_config = ConfigDict(from_attributes=True)

# --- 5. СХЕМИ ДЛЯ СКАРГ (COMPLAINTS) ---
class ComplaintCreate(BaseModel):
    BatchID: int
    message: str

class ComplaintResponse(BaseModel):
    ComplaintID: int
    message: str
    status: str
    CreatedDate: date
    model_config = ConfigDict(from_attributes=True)

# --- 6. СХЕМИ ДЛЯ РЕДАГУВАННЯ (UPDATE - PUT) ---
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class UserUpdate(BaseModel):
    FullName: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class BatchUpdate(BaseModel):
    Quantity: Optional[int] = None
    ExpirationDate: Optional[date] = None
    status: Optional[str] = None
class ManagerCreate(BaseModel):
    email: str
    password: str
    FullName: str
    role: str = "manager"
    StoreID: int