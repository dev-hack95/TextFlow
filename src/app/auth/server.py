import os
import sys
sys.path.append("src")
import jwt
import datetime
import psycopg2
import src.app.auth.models as models
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, requests, Request, Depends, status
from src.app.auth.db import get_db, engine
from src.logger import logging
from src.exception import CustomException
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        logging.info("Connecting to the database")
        conn = psycopg2.connect(host = '192.168.29.216',
                                port=5432,
                                database = 'auth_service',
                                user = 'postgres',
                                password = 'postgres',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        logging.info("Successfully connetced to database")
        break
    except Exception as err:
        logging.info('Error connecting to database')
        raise CustomException(err, sys)

@app.post("/login")
def login(db: Session = Depends(get_db)):
    auth = Request.auth
    if not auth:
        return {"message": "Not authenticated"}, 401
    
    # Check db for username and password
    

    
