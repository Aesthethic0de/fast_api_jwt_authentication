import secrets


class Db_config:
    Mongo_url = "mongodb+srv://user1:user1user1@cluster0.4n4j1jb.mongodb.net/?retryWrites=true&w=majority"
    Mongo_db = "fastapi"
    Mongo_collection = 'authenticate'

class Secret_Key:
    JWT_SECRET_KEY = secrets.token_hex(20)
    JWT_REFRESH_SECRET_KEY = secrets.token_hex(20)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30 #minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7