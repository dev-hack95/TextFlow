import os
import datetime
import models
from datetime import datetime
from fastapi import FastAPI, Request, Depends, status, HTTPException
from db import get_db, engine
from tokens import create_token, decode_token
from logger import logging
from exception import CustomException
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

secrets = "test12345"

@app.post("/v1/signin")
def signin(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Auth).filter(models.Auth.email == email).first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {email} already present in database")
    
    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least eight characters")
    
    new_user = models.Auth(email=email, password=password)
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}

@app.post("/v1/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Auth).filter(models.Auth.email == email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found, create a new account")
    
    if password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
   
    current_time = datetime.utcnow()

    if user.token is None:
        token = create_token(user.email, secrets, True)
        user.token = token
        db.commit()
    else:
        last_token_generated = user.created_at 
        last_token_generated = last_token_generated.replace(tzinfo=None)  
        difference = current_time - last_token_generated
        days_since_last_token = difference.days

        if days_since_last_token >= 44:
            token = create_token(user.email, secrets, True)
            user.token = token
            db.commit()
        else:
            token = user.token
    
    return {"message": "Logged in successfully"}, status.HTTP_200_OK
    

@app.post("/v1/validate")
def validate() -> str:
    encoded_jwt = Request.headers["Authorization"]

    if not encoded_jwt:
        return {"message": "Missing Credentials"}, 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = decode_token(encoded_token=encoded_jwt, secret=secrets)
    except:
        return {'message': f'Token is invalid'}, status.HTTP_401_UNAUTHORIZED
    
    return decoded, status.HTTP_200_OK
