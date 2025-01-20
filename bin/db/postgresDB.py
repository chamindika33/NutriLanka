from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.orm import Session
from fastapi import Depends
from bin.config import settings
# from bin.config import logConfig
from logging.config import dictConfig
import logging

pg_database: Session = None
engine = create_engine(str(settings.PG_URL) , future=True , pool_size=50 , max_overflow=10 , pool_recycle=1800)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
# pg_database: Session = scoped_session(SessionLocal)
# Session = scoped_session(SessionLocal) # Use scoped_session to ensure thread safety and proper session management


# Log Configs
# dictConfig(logConfig.dict())
logger = logging.getLogger("nutriLanka")

def db_connection():
    """
    *Postgres database connection
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        # Session.remove()  # Ensure the session is removed after use


Base = declarative_base()

pg_database: Session = Depends(db_connection())

try:
    with engine.connect() as connection:
        print("Database connection successful.")
except Exception as e:
    print(f"Database connection failed: {e}")