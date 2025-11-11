from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import Base, engine, SessionLocal
from app.models import models
from app.routers import user_router, transaction_router, prices, portfolio_router
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json

# WealthWise Portfolio Tracker API - Main Entry Point
app = FastAPI(title="WealthWise Portfolio Tracker API", version="1.0.0")

# Allow CORS (Optional - for frontend or Postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if using frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Initialization
Base.metadata.create_all(bind=engine)

# BACKGROUND JOB: Update Prices from mock_prices.json
def update_prices_from_json():
    """Reads mockdata.json and updates DB prices."""
    db = SessionLocal()
    try:
        file_path = os.path.join(os.path.dirname(__file__), "..", "mock_prices.json")
        with open(file_path, "r") as f:
            data = json.load(f)

        for entry in data:
            symbol = entry["symbol"]
            price = entry["current_price"]

            existing = db.query(models.Price).filter(models.Price.symbol == symbol).first()
            if existing:
                existing.current_price = price
            else:
                new_price = models.Price(symbol=symbol, current_price=price)
                db.add(new_price)

        db.commit()
        print("[INFO] Prices updated from mockdata.json")

    except Exception as e:
        print(f"[ERROR] Price update failed: {e}")
    finally:
        db.close()


# Initialize background scheduler (runs every 2 minutes)
scheduler = BackgroundScheduler()
scheduler.add_job(update_prices_from_json, "interval", minutes=2) 
scheduler.start()

# Run once on startup
update_prices_from_json()

# Root Route
@app.get("/")
def root():
    return {"message": "WealthWise Portfolio Tracker API is running"}

# Routers
app.include_router(user_router.router)
app.include_router(transaction_router.router)
app.include_router(portfolio_router.router)
app.include_router(prices.router)

# Global Exception Middleware
@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )

#  Manual Trigger Endpoint (Manually updates the priice if the auto function dont work ) 
@app.post("/prices/update-mock")
def manual_update_prices():
    """
    Trigger mock_prices.json price update manually.
    Useful for testing without waiting 2 minutes.
    """
    try:
        update_prices_from_json()
        return {"status": "success", "message": "Prices updated from mockdata.json"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
# 
