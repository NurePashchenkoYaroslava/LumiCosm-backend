from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Твій URL з паролем (PostgreSQL)
DATABASE_URL = "postgresql://postgres:1236Fuck_@localhost:5432/cosmetics_db"

engine = create_engine(DATABASE_URL)

# Налаштування сесії
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функція для отримання доступу до БД (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()