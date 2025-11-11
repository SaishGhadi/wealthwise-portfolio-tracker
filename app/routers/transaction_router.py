from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models.models import Transaction, TransactionType, Price
from app.schemas.schemas import TransactionCreate
from app.utils.responses import success_response, error_response
from app.utils.exceptions import bad_request, not_found
from app.utils.deps import get_current_user
from app.models.models import User

router = APIRouter(prefix="/transaction", tags=["Transactions"])


@router.post("/", response_model=None)
def add_transaction(
    txn: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id

    # 1️⃣ Get current price for the symbol
    price_obj = db.query(Price).filter(Price.symbol == txn.symbol).first()
    if not price_obj:
        return not_found(f"No current price found for symbol '{txn.symbol}'")

    current_price = price_obj.current_price

    # 2️⃣ SELL validation — ensure user owns enough units
    if txn.type == TransactionType.SELL:
        total_buys = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.symbol == txn.symbol,
            Transaction.type == TransactionType.BUY
        ).all()

        total_sells = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.symbol == txn.symbol,
            Transaction.type == TransactionType.SELL
        ).all()

        owned_units = sum(t.units for t in total_buys) - sum(t.units for t in total_sells)
        if txn.units > owned_units:
            return bad_request("Not enough units to sell")

    # 3️⃣ Create new transaction with current price
    new_txn = Transaction(
        user_id=user_id,
        symbol=txn.symbol,
        type=txn.type,
        units=txn.units,
        price=current_price,   # Auto-fetched
        date=txn.date or date.today()
    )

    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)

    data = {
        "id": new_txn.id,
        "user_id": new_txn.user_id,
        "symbol": new_txn.symbol,
        "type": new_txn.type,
        "units": new_txn.units,
        "price": new_txn.price,
        "date": str(new_txn.date)
    }

    return success_response(data=data, message="Transaction added successfully")


@router.get("/all", response_model=None)
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    txns = db.query(Transaction).filter(Transaction.user_id == user_id).all()

    if not txns:
        return error_response(message="No transactions found for this user", status_code=404)

    txn_list = [
        {
            "id": t.id,
            "symbol": t.symbol,
            "type": t.type,
            "units": t.units,
            "price": t.price,
            "date": str(t.date)
        }
        for t in txns
    ]

    return success_response(data=txn_list, message="Transactions retrieved successfully")
