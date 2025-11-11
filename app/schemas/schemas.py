from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from enum import Enum
from typing import Optional


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


# Schema for Creating New User
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None

# Schema for Creating New TRANSACTION


class TransactionCreate(BaseModel):
    # user_id: int
    symbol: str
    type: TransactionType
    units: float
    date: date


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    type: TransactionType
    units: float
    price: float
    date: date

    class Config:
        orm_mode = True


class PriceResponse(BaseModel):
    symbol: str
    current_price: float

    class Config:
        orm_mode = True
