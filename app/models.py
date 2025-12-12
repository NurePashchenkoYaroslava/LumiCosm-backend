from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Store(Base):
    __tablename__ = "stores"
    StoreID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    users = relationship("User", back_populates="store") 
    batches = relationship("Batch", back_populates="store", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True, index=True)
    FullName = Column(String)
    role = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    StoreID = Column(Integer, ForeignKey("stores.StoreID"), nullable=True)
    store = relationship("Store", back_populates="users")
    scans = relationship("ScanHistory", back_populates="user", cascade="all, delete-orphan") 
    complaints = relationship("Complaint", back_populates="user", cascade="all, delete-orphan") 

class Product(Base):
    __tablename__ = "products"
    ProductID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    category = Column(String)
    description = Column(Text)
    batches = relationship("Batch", back_populates="product", cascade="all, delete-orphan")

class Batch(Base):
    __tablename__ = "batches"
    BatchID = Column(Integer, primary_key=True, index=True)
    StoreID = Column(Integer, ForeignKey("stores.StoreID"))
    ProductID = Column(Integer, ForeignKey("products.ProductID"))
    qr_code = Column(String, unique=True, index=True) 
    ManufactureDate = Column(Date)
    ExpirationDate = Column(Date)
    Quantity = Column(Integer)
    Certificate = Column(String, nullable=True)  
    status = Column(String, default="active")  
    product = relationship("Product", back_populates="batches") 
    store = relationship("Store", back_populates="batches")
    scans = relationship("ScanHistory", back_populates="batch", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="batch", cascade="all, delete-orphan")

class ScanHistory(Base):
    __tablename__ = "scan_history"
    ScanHistoryID = Column(Integer, primary_key=True, index=True)
    ScanTime = Column(DateTime(timezone=True), server_default=func.now()) 
    UserID = Column(Integer, ForeignKey("users.UserID"))
    BatchID = Column(Integer, ForeignKey("batches.BatchID"))
    user = relationship("User", back_populates="scans")
    batch = relationship("Batch", back_populates="scans")

class Complaint(Base):
    __tablename__ = "complaints"
    ComplaintID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("users.UserID"))
    BatchID = Column(Integer, ForeignKey("batches.BatchID"))
    message = Column(String)  
    status = Column(String, default="new")  
    CreatedDate = Column(Date, default=func.now())
    user = relationship("User", back_populates="complaints") 
    batch = relationship("Batch", back_populates="complaints")