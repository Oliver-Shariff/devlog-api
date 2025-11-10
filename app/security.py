from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app.models import User
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
import os
from datetime import datetime, timedelta, timezone

from app.database import get_db

load_dotenv()

JWT_SECRET=os.getenv("JWT_SECRET")
JWT_ALG=os.getenv("JWT_ALG")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    user = db.get(User,email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm= JWT_ALG)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    ) -> User:
    """ Decode JWT, extract subject (email), fetch user. Raise 401 if token is invalid or user doesn't exist """
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials",
    headers={"WWW-Authenticate":"Bearer"},
    )

    try:
        payload = jwt.decode(token,JWT_SECRET, algorithms=[JWT_ALG])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = db.get(User, email)
    if not user:
        raise credentials_exception

    return user