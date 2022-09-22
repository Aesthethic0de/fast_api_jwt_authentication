import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from config import Secret_Key

ACCESS_TOKEN_EXPIRE_MINUTES = Secret_Key.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = Secret_Key.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM = Secret_Key.ALGORITHM
JWT_SECRET_KEY = Secret_Key.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = Secret_Key.JWT_REFRESH_SECRET_KEY  # should be kept secret


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


