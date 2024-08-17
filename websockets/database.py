from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://usersapi_rk0r_user:iBaiCtjVPV63IPeudXOoslwnDjnS5AVB@dpg-col7h0tjm4es738c6cl0-a.oregon-postgres.render.com/usersapi_rk0r"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()