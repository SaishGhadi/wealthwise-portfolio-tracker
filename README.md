
---

# WealthWise Portfolio Tracker API

**Author:** Saish Ghadi

**Tech Stack:** FastAPI · PostgreSQL · SQLAlchemy

**Project Type:** Backend API 

---

##  Overview

**WealthWise Portfolio Tracker** is a backend API service designed to manage user investment portfolios.
It allows users to record **stock transactions (buy/sell)**, view their **current holdings**, and calculate **profit or loss** based on real-time or mock market prices.

This project demonstrates **backend API development**, **database modeling**, and **portfolio computation logic** using modern Python frameworks.

---

##  Features

* User registration and authentication
* Record **buy/sell** stock transactions
* Fetch **real-time or mock** stock prices
* Generate **portfolio summary** with total value and profit/loss
* Consistent JSON API responses
* Clean, modular architecture using **routers**, **schemas**, and **utility helpers**

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/SaishGhadi/wealthwise-portfolio-tracker.git
cd wealthwise-portfolio-tracker
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

Create a database named **wealthwise_db**:

```sql
CREATE DATABASE wealthwise_db;
```

### 5. Configure Environment Variables

Create a `.env` file in the project root (Make sure to include the password used in pgAdmin):

```
DATABASE_URL=postgresql://postgres:<password>@localhost/wealthwise_db
```

>  If your password includes special characters (like `@` or `#`), use URL encoding (e.g., `@` → `%40`, `#` → `%23`).

### 6. Run the Server

```bash
uvicorn app.main:app --reload
```

Server will run at:
 [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger UI (API Docs):
 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔗 API Endpoints

| Method   | Endpoint              | Description                                                                                                                                                               | Auth Required |
| -------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| **POST** | `/user`               | Register a new user with name, email, and password. Passwords are securely hashed using bcrypt.                                                                           | NO             |
| **POST** | `/user/login`         | Authenticate user and return a JWT token for further requests.                                                                                                            | NO             |
| **GET**  | `/user`               | Fetch all registered users.                                                                                                                                               | NO             |
| **POST** | `/transaction`        | Add a new **BUY/SELL** transaction for the logged-in user. The system automatically fetches the current price from the `prices` table (users don’t enter price manually). | YES            |
| **GET**  | `/transaction/all`    | Fetch all transactions for the logged-in user.                                                                                                                            | YES            |
| **GET**  | `/portfolio-summary`  | Calculate and return the user’s holdings, total portfolio value, and unrealized profit/loss based on current prices.                                                      | YES            |
| **GET**  | `/prices`             | Fetch the current prices for all symbols in the system.                                                                                                                   | NO             |
| **POST** | `/prices/update-mock` | Manually trigger the price update from `mock_prices.json` file (useful for testing the background job).                                                                   | NO             |
| **GET**  | `/`                   | Root route — confirms that the WealthWise API is running.                                                                                                                 | NO             |

---

### 🔒 Authentication Notes

* All endpoints marked ✅ require a valid JWT token.
* To authenticate:

  1. Call `/user/login` to get your token.
  2. In Swagger UI, click **Authorize** and paste **only the token (not “Bearer”)**.
  3. Swagger will automatically send your token for all secure requests.

---

##  Final API Endpoints
##
<img width="1331" height="731" alt="image" src="https://github.com/user-attachments/assets/2e1ddf02-c998-4383-ad90-a5d440261ede" />

---

##  Example Response

### **GET /portfolio-summary?user_id=1**

```json
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
```

---

##  Database Schema

### **users**

| Field      | Type         | Description           |
| ---------- | ------------ | --------------------- |
| id         | int (PK)     | Unique user ID        |
| name       | varchar(100) | User’s name           |
| email      | varchar(100) | Unique email          |
| password   | varchar(255) | Hashed password       |
| created_at | timestamp    | Account creation time |

### **transactions**

| Field   | Type        | Description      |
| ------- | ----------- | ---------------- |
| id      | int (PK)    | Transaction ID   |
| user_id | int (FK)    | Linked user      |
| symbol  | varchar(50) | Stock symbol     |
| type    | varchar(10) | BUY or SELL      |
| units   | float       | Quantity         |
| price   | float       | Price per unit   |
| date    | date        | Transaction date |

### **prices**

| Field         | Type             | Description          |
| ------------- | ---------------- | -------------------- |
| symbol        | varchar(50) (PK) | Stock symbol         |
| current_price | float            | Current market price |

---
Perfect — adding a **DFD (Data Flow Diagram)** section to your README will make your backend project documentation look much more professional.

Here’s the section you can **copy-paste directly** into your `README.md`:

---

##  Data Flow Diagram (DFD)

The following diagram represents the logical flow of data within the **WealthWise Portfolio Tracker** backend.
It shows how user actions interact with various API endpoints, how data moves between routes and the database, and how background processes keep information updated.

There isn’t much visual to show in a backend project — it’s all about how data flows, interacts, and stays consistent behind the scenes, which is exactly what this DFD highlights.

##
<img width="3569" height="1581" alt="WN dfd-2025-11-12-151346" src="https://github.com/user-attachments/assets/a84a5258-ab2c-45c6-a2ef-5b7ea87ae081" />




---

##  Project Structure

```
app/
│
├── main.py                          # Entry point of the FastAPI app
├── database.py                      # SQLAlchemy DB engine and session
│
├── models/
│   └── models.py                    # User, Transaction, and Price models
│
├── routers/
│   ├── user_router.py               # Handles user registration and login
│   ├── transaction_router.py        # Buy/Sell transactions (JWT-protected)
│   ├── portfolio_router.py          # Portfolio value and profit/loss endpoints
│   └── prices.py                    # Price listing and mock price update API
│
├── schemas/
│   └── schemas.py                   # Pydantic request/response schemas
│
├── utils/
│   ├── auth.py                      # Password hashing + JWT creation/verification
│   ├── deps.py                      # Token validation dependency (get_current_user)
│   ├── exceptions.py                # Custom reusable HTTP error handlers
│   └── responses.py                 # Unified API response format
│
├── mock_prices.json                 # Mock price data for initial load or testing
│
└── requirements.txt                 # Project dependencies
```

---

##  Testing

You can test all API routes directly using FastAPI's built-in Swagger UI or Postman.

Using Swagger UI

Visit:

http://127.0.0.1:8000/docs


### **Using Postman**

A Postman collection (`WealthWise.postman_collection.json`) is included.
Import it into Postman and test the endpoints in the following order:

---

#### **1️ Create User (POST)**

```
http://127.0.0.1:8000/users
```

---

#### **2️ Add Transaction (POST)**

```
http://127.0.0.1:8000/transection
```

![Add Transaction Screenshot](https://github.com/user-attachments/assets/0d452fd4-fb43-4e87-9bd5-162d1d219671)

---

#### **3️ Show All Transactions (GET)**

```
http://127.0.0.1:8000/transection/all?user_id=1
```

![All Transactions Screenshot](https://github.com/user-attachments/assets/249eb654-46e4-463e-81a0-13a3e70d392e)

---

#### **4️ Fetch Portfolio Summary (GET)**

```
/portfolio-summary?user_id=1
```

**(Prices Table)**
###
![Prices Table Screenshot](https://github.com/user-attachments/assets/a226437d-5257-4b7d-8087-fb0113ffd9e7)

**(Summary)**
###
![Portfolio Summary Screenshot](https://github.com/user-attachments/assets/dffa5da1-e5d3-4e82-a54a-42b1086052f5)

---

### **After Updating Prices**

```sql
UPDATE prices SET current_price = 3600 WHERE symbol = 'TCS';
UPDATE prices SET current_price = 1580 WHERE symbol = 'INFY';
```

**(Updated Prices Table)**

![Updated Prices Screenshot](https://github.com/user-attachments/assets/50e799aa-d5e0-4d2a-9e7c-35628b80bd48)

**(Updated Summary)**

![Updated Summary Screenshot](https://github.com/user-attachments/assets/001dcafd-51e5-4346-8768-88ba537fdaf9)


---

##  JWT Authentication & Secure Access

The WealthWise API now includes secure user authentication using **JWT (JSON Web Tokens)** and **bcrypt password hashing**.

### **Features Implemented**

* User registration with **hashed password storage** (bcrypt).
* **Login endpoint** (`POST /user/login`) that verifies user credentials and returns a JWT token.
* **Protected routes** (`/transaction`, `/portfolio-summary`) accessible only with a valid token.
* Automatic **token-based user identification** — no need to manually pass `user_id` in requests.
* **CORS-enabled backend** for frontend or Postman integration.

---

### **Password Security**

* Passwords are hashed using `bcrypt` with automatic salt generation.
* Plain-text passwords are never stored in the database.

Example of a stored bcrypt hash:

```
$2b$12$ZRhV7v3sKsfmReXgc.xZB.8Xy3u8sbjLOixD4zM0.Y.IkEE4clAO6
```

---

### **Login & Token Generation**

**Endpoint:**

```
POST /user/login
```

**Request (form data):**

```
username: saish@example.com
password: test123
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  },
  "message": "Login successful"
}
```

---

### **Authentication Flow**

1. **Register** a new user via `POST /user`

   ```json
   {
     "name": "Saish Ghadi",
     "email": "saish@example.com",
     "password": "test123"
   }
   ```

2. **Login** via `POST /user/login` to get a JWT token.

```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE3NjI4NzE0MjR9.QqMi18O1jaAYeCVl9rnarnw2ceOjYM3H5zdgk-lHQAo",
    "token_type": "bearer"
  },
  "message": "Login successful"
}
```
   

4. Copy the `access_token` and **authorize** in Swagger UI (top-right “Authorize” button):


   ###
   <img width="583" height="240" alt="image" src="https://github.com/user-attachments/assets/cde01e3c-d33f-4514-8fcf-310261ec7e8e" />

   

5. Now all protected endpoints (like `/transaction/all` or `/portfolio-summary`) will work using that token.

---

### **Protected Routes Example**

**Headers required:**

```
Authorization: Bearer <your_token_here>
```

**Example call:**

```
GET /transaction/all
```

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "symbol": "TCS",
      "type": "BUY",
      "units": 5,
      "price": 3400,
      "date": "2025-11-08"
    }
  ],
  "message": "Transactions retrieved successfully"
}
```

---

### **Security Highlights**

* JWT tokens include expiry (`exp` claim).
* Tokens are signed using HS256 algorithm and `SECRET_KEY`.
* Invalid or expired tokens return a `401 Unauthorized` response.
* All password operations use bcrypt-safe comparison (`bcrypt.checkpw`).
* 
---

### **What i Added in This Stage**

| Feature                       | Description                                                       |
| ----------------------------- | ----------------------------------------------------------------- |
| **bcrypt Hashing**            | Passwords securely stored with salt-based hashes.                 |
| **JWT Login Endpoint**        | `/user/login` implemented for authentication.                     |
| **Token Generation & Expiry** | JWT created with expiry and user_id payload.                      |
| **Protected Routes**          | `/transaction` and `/portfolio-summary` now require valid tokens. |
| **Auto User Resolution**      | Authenticated user automatically identified in every request.     |
| **Swagger Authorization**     | Integrated “Authorize” flow to test protected endpoints easily.   |

---

##  Background Price Auto-Update Feature

To make the portfolio more realistic, the API includes an automated price refresh mechanism that periodically updates asset prices in the database.

### How it works:

* The feature is implemented using **APScheduler** (Advanced Python Scheduler).
* Every 2 minutes (can change in code), a background job runs the `update_prices()` function.
* This function fetches all entries from the `prices` table and simulates live market behavior by slightly fluctuating each stock’s price (±5%).
* The change is small and random to resemble real-time market volatility.
* The updated prices are saved to the database, so users always see near-live mock values when fetching prices or calculating portfolio value.

### Why it’s useful:

* Helps simulate a **dynamic market environment** without relying on real APIs.
* Ensures the portfolio and transaction calculations use changing data.
* Keeps your project realistic and suitable for **demo or testing purposes**.



---

##  Author

**Saish Ghadi**

---


