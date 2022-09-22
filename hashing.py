from passlib.context import CryptContext
password_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def get_hashed_password(password : str) -> str:
    return password_context.hash(password)

def verify_password(password : str, hashedpassword : str) -> str:
    return password_context.verify(password,hashedpassword)



