from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

# Enum for transaction type
class TransactionType(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(255), nullable=True)   # new column (hashed) added for jwt authententication 
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to transactions
    transactions = relationship("Transaction", back_populates="user")


# Transaction Model 
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    symbol = Column(String, ForeignKey("prices.symbol", ondelete="CASCADE"))
    type = Column(Enum(TransactionType), nullable=False)
    units = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    # Relationships
    user = relationship("User", back_populates="transactions")


# Prices Model 
class Price(Base):
    __tablename__ = "prices"

    symbol = Column(String, primary_key=True)
    current_price = Column(Float, nullable=False)


