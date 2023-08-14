from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger import logging
from dotenv import load_dotenv
from exception import CustomException
import socket
import sys
import os

load_dotenv("./.env")
#ip_addr = socket.gethostbyname(socket.gethostname())

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        logging.info("Connecting to database")
        yield db
    except Exception as err:
        logging.info("Error occured while connecting to database")
        raise CustomException(err, sys)
    finally:
        db.close()
        logging.info("Closing the connection")
