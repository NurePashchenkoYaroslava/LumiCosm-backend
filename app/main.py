from fastapi import FastAPI
from .routers import auth, admin, manager, scanner 
from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LumiCosm System API")

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(manager.router)
app.include_router(scanner.router)

@app.get("/")
def root():
    return {"message": "Server is running. Go to /docs for API interface"}