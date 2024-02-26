from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger import logging
from dotenv import load_dotenv
from exception import CustomException
import sys
import os

load_dotenv()
db_user = 'postgres' #os.getenv("POSTGRES_USER")
db_password = 'postgres' #os.getenv("POSTGRES_PASSWORD")
db_host = '192.168.43.86' #os.getenv("POSTGRES_HOST")
db_name = 'postgres' #os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    return db
//This is Database Session
