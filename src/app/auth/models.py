from src.app.auth.db import Base
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP
from sqlalchemy.sql import func

class Auth(Base):

    __tablename__ = "auth_details"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
