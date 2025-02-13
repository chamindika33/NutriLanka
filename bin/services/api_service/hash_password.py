from passlib.context import CryptContext
from bin.models import pg_models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(pw: str, hash_pw: str) -> bool:
    return pwd_context.verify(pw, hash_pw)

def hash_password(password):
    return pwd_context.hash(password)