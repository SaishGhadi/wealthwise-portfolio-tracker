from app.utils.exceptions import not_found
from app.utils.responses import success_response, error_response
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Transaction, Price, TransactionType
from app.utils.deps import get_current_user

router = APIRouter(prefix="/portfolio-summary", tags=["Portfolio Summary"])


@router.get("/")
def get_portfolio_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    #  Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return not_found("User not found")

    # Fetch transactions
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    if not transactions:
        return error_response("No transactions found for this user.", 404)

    #  Group by symbol
    portfolio = {}
    for txn in transactions:
        if txn.symbol not in portfolio:
            portfolio[txn.symbol] = {"buy_units": 0, "buy_cost": 0, "sell_units": 0}
        if txn.type == TransactionType.BUY:
            portfolio[txn.symbol]["buy_units"] += txn.units
            portfolio[txn.symbol]["buy_cost"] += txn.units * txn.price
        elif txn.type == TransactionType.SELL:
            portfolio[txn.symbol]["sell_units"] += txn.units

    #  Fetch current prices
    prices = {p.symbol: p.current_price for p in db.query(Price).all()}

    #  Calculate holdings
    holdings = []
    total_value = 0
    total_gain = 0

    for symbol, data in portfolio.items():
        net_units = data["buy_units"] - data["sell_units"]
        if net_units <= 0:
            continue

        avg_cost = data["buy_cost"] / data["buy_units"] if data["buy_units"] > 0 else 0
        current_price = prices.get(symbol, 0)
        current_value = net_units * current_price
        unrealized_pl = (current_price - avg_cost) * net_units

        holdings.append({
            "symbol": symbol,
            "units": net_units,
            "avg_cost": round(avg_cost, 2),
            "current_price": current_price,
            "unrealized_pl": round(unrealized_pl, 2)
        })

        total_value += current_value
        total_gain += unrealized_pl

    #  Final summary
    data = {
        "user_id": user_id,
        "holdings": holdings,
        "total_value": round(total_value, 2),
        "total_gain": round(total_gain, 2)
    }

    return success_response(data=data, message="Portfolio summary fetched successfully")
