import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "123242422978656456745678")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour


# ================================
# PASSWORD HASHING / VERIFICATION
# ================================
def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt (utf-8 encoded).
    Automatically generates a random salt.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    password = password.strip().encode("utf-8")[:72]  # enforce bcrypt limit
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode("utf-8")  # store as string in DB


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against its bcrypt hash.
    """
    if not plain_password or not hashed_password:
        return False

    plain_password = plain_password.strip().encode("utf-8")[:72]
    hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password, hashed_password)


# ================================
# JWT CREATION / VALIDATION
# ================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT token with expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decodes and validates JWT token.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
