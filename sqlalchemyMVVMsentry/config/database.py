from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

# Database connection details (replace with your credentials)
pgInfo = os.getenv('POSTGRESQL_KEY')
DATABASE_URL = pgInfo
engine = create_engine(DATABASE_URL)
# connection details (replace with your credentials)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Modelos 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()