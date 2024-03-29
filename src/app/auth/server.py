import os
from datetime import datetime, timezone
from typing import Literal
import models
from fastapi import FastAPI, Request, Depends, status, HTTPException
from datetime import datetime
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
   
    token = create_token(user.email, secrets, True)
    return token, status.HTTP_200_OK
    

@app.post("/v1/validate")
def validate(request: Request):
    encoded_jwt = request.headers.get("Authorization")
    if not encoded_jwt:
        return {"message": "Missing Credentials"}, status.HTTP_401_UNAUTHORIZED
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_jwt, secrets, algorithms=["HS256"])
    except jwt.exceptions.DecodeError as err:
        if "Expiration Time claim (exp) must be an integer" in str(err):
            decoded = jwt.decode(encoded_jwt, secrets, algorithms=["HS256"], options={"verify_exp": False})
            exp_claim = decoded.get("exp")
            if exp_claim is not None and isinstance(exp_claim, str):
                decoded["exp"] = int(datetime.fromisoformat(exp_claim).replace(tzinfo=timezone.utc).timestamp())
        else:
            raise err

    
    return decoded
