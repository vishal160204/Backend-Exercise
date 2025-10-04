from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from app.config import DATABASE_URL


engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/offset_db")

SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()