from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger import logging
from dotenv import load_dotenv
from exception import CustomException
import sys

load_dotenv("./.env")
#ip_addr = socket.gethostbyname(socket.gethostname())
engine = create_engine("postgresql://postgres:postgres@192.168.29.217/auth_service")
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
