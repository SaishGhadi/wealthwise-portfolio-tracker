from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Transaction, User, TransactionType
from app.schemas.schemas import TransactionCreate, TransactionResponse
from typing import List
from app.utils.responses import success_response, error_response
from app.utils.exceptions import bad_request

router = APIRouter(prefix="/transaction", tags=["Transactions"])


# ===== Add Transaction =====
@router.post("/", response_model=TransactionResponse)
def add_transaction(txn: TransactionCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == txn.user_id).first()
    if not user:
        bad_request("User not found")

    # SELL validation  ensure user owns enough units
    if txn.type == TransactionType.SELL:
        total_buys = db.query(Transaction).filter(
            Transaction.user_id == txn.user_id,
            Transaction.symbol == txn.symbol,
            Transaction.type == TransactionType.BUY
        ).all()

        total_sells = db.query(Transaction).filter(
            Transaction.user_id == txn.user_id,
            Transaction.symbol == txn.symbol,
            Transaction.type == TransactionType.SELL
        ).all()

        owned_units = sum(t.units for t in total_buys) - \
            sum(t.units for t in total_sells)
        if txn.units > owned_units:
            bad_request("Not enough units to sell")

    new_txn = Transaction(
        user_id=txn.user_id,
        symbol=txn.symbol,
        type=txn.type,
        units=txn.units,
        price=txn.price,
        date=txn.date
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return success_response(message="Transaction added successfully")


#  Get Transaction History
@router.get("/all", response_model=List[TransactionResponse])
def get_transactions(user_id: int = Query(...), db: Session = Depends(get_db)):
    txns = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    if not txns:
        bad_request("No transactions found for this user")
    return txns
