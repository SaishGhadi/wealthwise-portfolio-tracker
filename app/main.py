from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.models import models
from app.routers import user_router, transaction_router, prices, portfolio_router
from fastapi.middleware.cors import CORSMiddleware

# WealthWise Portfolio Tracker API - Main Entry Point

app = FastAPI(title="WealthWise Portfolio Tracker API", version="1.0.0")


# Allow CORS (Optional - for frontend or Postman)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if using a frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Initialization

Base.metadata.create_all(bind=engine)


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
