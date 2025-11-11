from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse
from app.utils.auth import hash_password, verify_password, create_access_token
from app.utils.responses import success_response, error_response
from datetime import timedelta

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", response_model=None)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pwd = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(
        data={"id": new_user.id, "email": new_user.email},
        message="User registered successfully",
    )


@router.post("/login")
def login_user(
    useremail: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token."""
    user = db.query(User).filter(User.email == useremail).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=60)
    token = create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires)

    return success_response(
        data={"access_token": token, "token_type": "bearer"},
        message="Login successful",
    )


@router.get("/", response_model=None)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return success_response(data=users, message="All users fetched successfully")
