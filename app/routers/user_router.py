from app.utils.auth import verify_password, create_access_token
from app.utils.exceptions import bad_request
from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse, Token
from app.utils.responses import success_response, error_response
from app.utils.exceptions import bad_request, not_found
from app.utils.auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import os

router = APIRouter(prefix="/user", tags=["Users"])

# Create user (register)


@router.post("/", response_model=None)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        return bad_request("Email already exists")

    hashed = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(data={"id": new_user.id, "email": new_user.email}, message="User created successfully")


# Login endpoint - returns JWT

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login using username (email) and password.
    Returns JWT token on success.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        return bad_request("Invalid email or password")

    if not verify_password(form_data.password, user.password):
        return bad_request("Invalid email or password")

    access_token_expires = timedelta(minutes=int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)))
    token = create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires)

    return success_response(
        data={"access_token": token, "token_type": "bearer"},
        message="Login successful"
    )
