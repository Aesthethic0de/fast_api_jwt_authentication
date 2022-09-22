from fastapi import FastAPI, status, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel

import config
from hashing import get_hashed_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import pymongo
from jwt_token_generation import create_access_token, create_refresh_token
from uuid import uuid4, UUID
from schema import UserOut,SystemUser,TokenSchema,TokenPayload,User_Authenticate
from deps import current_user, reusable_authentication
import uvicorn
from config import Db_config

client = pymongo.MongoClient(Db_config.Mongo_url)
db = client[Db_config.Mongo_db]
coll = db[Db_config.Mongo_collection]

app = FastAPI()

@app.post("/signup", response_model=UserOut)
async def enter_details(user : User_Authenticate):
    check = coll.find_one({"username":user.username, "email" : user.email})
    if check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
      )
    hashed_password = get_hashed_password(password=user.password)
    user_object = dict(user)
    user_object['password'] = hashed_password
    user_object['id'] = str(uuid4())
    coll.insert_one(user_object)
    return user_object

@app.post('/login', response_model=TokenSchema)
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = coll.find_one({"username": request.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="login username not found"
        )
    access_token = create_access_token(user["username"])
    refresh_token = create_refresh_token(user["username"])
    user_hashed = user['password']
    if verify_password(password=request.password,hashedpassword=user_hashed):
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

@app.get("/me", response_model=UserOut)
async def get_me(user : UserOut = Depends(current_user)):
    return user


#test endpoint
@app.post("/get_images")
async def get_images(file: UploadFile, user : UserOut = Depends(current_user)):
    file_name = file.filename
    return {"filename" : file_name}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9092)
