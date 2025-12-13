from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, crud

router = APIRouter(prefix="/auth", tags=["Auth & Registration"])

@router.post("/register", response_model=schemas.UserResponse) 
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email вже зареєстрован")
    
    return crud.create_user(db=db, user=user)

@router.post("/login")
def login(login_data: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, email=login_data.email)
    if not user or user.password != login_data.password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    return {"message": "Login successful", "user_id": user.UserID, "role": user.role}