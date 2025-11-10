from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from app.database import Base, engine
from app.models import models
from app.routers import user_router, transaction_router, prices
from app.routers import portfolio_router


app = FastAPI(title="WealthWise Portfolio Tracker API")


# Creates all tables
Base.metadata.create_all(bind=engine)

#   root
@app.get("/")
def root():
    return {"message": "WealthWise Portfolio Tracker API is running "}


# Includes routers
app.include_router(user_router.router)
app.include_router(portfolio_router.router)
app.include_router(prices.router)
app.include_router(transaction_router.router)


@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )
