from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger import logging
from exception import CustomException
import sys
import os


db_user = os.environ.get("POSTGRES_USER")
db_password = os.environ.get("POSTGRES_PASSWORD")
db_host = os.environ.get("POSTGRES_HOST")
db_name = os.environ.get("POSTGRES_DB")

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
