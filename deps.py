from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt_token_generation import JWT_SECRET_KEY, ALGORITHM
from jose import jwt
from pydantic import ValidationError
import pymongo
from schema import UserOut,SystemUser,TokenSchema,TokenPayload,User_Authenticate
from config import Db_config


client = pymongo.MongoClient(Db_config.Mongo_url)
db = client[Db_config.Mongo_db]
coll = db[Db_config.Mongo_collection]
reusable_authentication = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

async def current_user(token : str = Depends(reusable_authentication)) ->SystemUser:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired",
                                headers={"WWW-Authenticate" : " Bearer"},
                                )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    user = coll.find_one({"username": token_data.sub})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return UserOut(**user)