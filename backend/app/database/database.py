from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./portfolio.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create the declarative base class
Base = declarative_base()

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)