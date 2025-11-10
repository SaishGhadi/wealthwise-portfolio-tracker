WealthWise Portfolio Tracker API

Author: Saish Ghadi
Tech Stack: FastAPI · PostgreSQL · SQLAlchemy
Project Type: Backend API Assignment

Overview

WealthWise Portfolio Tracker is a backend service designed to manage user investment portfolios.
It allows users to record stock transactions (buy/sell), view their current holdings, and calculate profit or loss based on real-time or mock market prices.

This project demonstrates backend API development, database design, and portfolio computation logic using modern Python frameworks.

Features

User registration and management

Record buy/sell transactions for stocks

Fetch real-time or mock prices from the database

Portfolio summary calculation with total value and unrealized profit/loss

Consistent API response structure

Modular architecture using routers and utility helpers

Setup Instructions

1. Clone the Repository
   git clone <your_repo_url>
   cd wealthwise-portfolio-tracker

2. Create Virtual Environment
   python -m venv venv
   venv\Scripts\activate # On Windows
   source venv/bin/activate # On macOS/Linux

3. Install Dependencies
   pip install -r requirements.txt

4. Setup Database

Create a PostgreSQL database named wealthwise_db:

CREATE DATABASE wealthwise_db;

5. Configure Environment

Create a .env file in the project root:

DATABASE_URL=postgresql://postgres:<password>@localhost/wealthwise_db

6. Run the Server
   uvicorn app.main:app --reload

The API will be available at
http://127.0.0.1:8000

Open the interactive documentation at
http://127.0.0.1:8000/docs

API Endpoints
Method Endpoint Description
POST /user Create a new user
GET /transaction/all?user_id=<id> Fetch all transactions for a user
POST /transaction Add a buy/sell transaction
GET /portfolio-summary?user_id=<id> Get portfolio summary for a user
Example Response

GET /portfolio-summary?user_id=1

{
"status": "success",
"data": {
"user_id": 1,
"holdings": [
{
"symbol": "TCS",
"units": 12,
"avg_cost": 3400,
"current_price": 3600,
"unrealized_pl": 2400
}
],
"total_value": 43200,
"total_gain": 2400
},
"message": "Portfolio summary fetched successfully"
}

Database Schema
users
Field Type Description
id int (PK) Unique user ID
name varchar(100) User’s name
email varchar(100) Unique email
password varchar(255) Hashed password
created_at timestamp Account creation time
transactions
Field Type Description
id int (PK) Transaction ID
user_id int (FK) Linked user
symbol varchar(50) Stock symbol
type varchar(10) BUY or SELL
units float Quantity
price float Price per unit
date date Transaction date
prices
Field Type Description
symbol varchar(50) (PK) Stock symbol
current_price float Current market price


Project Structure
app/
├── main.py
├── database.py
├── models/
│ └── models.py
├── routers/
│ ├── user_router.py
│ ├── transaction_router.py
│ └── portfolio_router.py
├── utils/
│ ├── exceptions.py
│ └── responses.py
└── mock_prices.json

Testing

You can test all API routes directly using FastAPI's built-in Swagger UI or Postman.

Using Swagger UI

Visit:

http://127.0.0.1:8000/docs

Using Postman

A Postman collection (WealthWise.postman_collection.json) is included.
Import it into Postman and test the endpoints in the following order:

Create User

Add Transactions

Fetch Portfolio Summary

Author

Saish Ghadi
Bachelor of Engineering in Information Technology
Goa Engineering College
