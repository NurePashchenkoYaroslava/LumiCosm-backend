from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, crud

router = APIRouter(prefix="/admin", tags=["System Administrator"])


@router.post("/add_store")
def add_store(store: schemas.StoreCreate, db: Session = Depends(database.get_db)):
    new_store = crud.create_store(db=db, store=store)
    return {
        "message": "Магазин успішно додано",
        "store_id": new_store.StoreID
    }
@router.post("/add_product")
def add_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    new_product = crud.create_product(db=db, product=product)
    return {
        "message": "Продукт додано в каталог",
        "product_id": new_product.ProductID
    }

@router.post("/register_manager", response_model=schemas.UserResponse)
def register_manager(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if user.role != "manager":
        raise HTTPException(status_code=400, detail="This endpoint is for managers only")
    if user.StoreID is None:
        raise HTTPException(status_code=400, detail="Manager must be assigned to a Store ID")    
    store = db.query(models.Store).filter(models.Store.StoreID == user.StoreID).first()
    
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    return crud.create_user(db=db, user=user)
@router.delete("/stores/{store_id}")
def delete_store(store_id: int, db: Session = Depends(database.get_db)):
    deleted = crud.delete_store(db, store_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Store not found")
    return {"message": f"Store {store_id} deleted"}

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product {product_id} deleted"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted"}

@router.put("/stores/{store_id}/update_address")
def update_store(store_id: int, new_address: str, db: Session = Depends(database.get_db)):
    updated = crud.update_store_address(db, store_id, new_address)
    if not updated:
        raise HTTPException(status_code=404, detail="Store not found")
    return {"message": "Address updated", "store": updated}

@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product_details(product_id: int, updates: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    updated_product = crud.update_product(db, product_id, updates)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user_details(user_id: int, updates: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    updated_user = crud.update_user(db, user_id, updates)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user