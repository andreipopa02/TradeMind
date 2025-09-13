import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('EMAIL_TOKEN_SECRET_KEY')
ALGORITHM = os.getenv('EMAIL_TOKEN_ALGORITHM')
TOKEN_EXPIRE_MINUTES = int(os.getenv('EMAIL_TOKEN_EXPIRE_MINUTES'))

used_reset_tokens = set()

def create_token_email(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token_email(token: str) -> dict:
    if token in used_reset_tokens:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None