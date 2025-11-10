from app.utils.exceptions import not_found, bad_request
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse
from typing import List
from app.utils.responses import success_response, error_response
from app.utils.exceptions import bad_request

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        bad_request("Email already exists with this email")

    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return success_response(data={"id": new_user.id, "email": new_user.email}, message="User created successfully")


# Get all users
@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        not_found("User with given ID not found")
    return {"status": "success", "data": user}
