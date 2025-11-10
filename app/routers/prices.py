from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Price
from app.schemas.schemas import PriceResponse
from typing import List

router = APIRouter(prefix="/prices", tags=["Prices"])

# Get all stocks and their prices
@router.get("/", response_model=List[PriceResponse])
def get_all_prices(db: Session = Depends(get_db)):
    prices = db.query(Price).all()
    return prices
