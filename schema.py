from pydantic import BaseModel
from uuid import UUID

class UserOut(BaseModel):
    id: UUID
    email: str
    username: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class User_Authenticate(BaseModel):
    username : str
    password : str
    email : str

class check_login(BaseModel):
    username : str
    password : str

class SystemUser(BaseModel):
    password: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None