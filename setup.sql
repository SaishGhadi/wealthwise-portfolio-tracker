-- Create Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,           -- Added for JWT authentication
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Prices table
CREATE TABLE prices (
    symbol VARCHAR(50) PRIMARY KEY,
    current_price FLOAT NOT NULL
);

-- Create Transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    symbol VARCHAR(50) REFERENCES prices(symbol) ON DELETE CASCADE,
    type VARCHAR(10) CHECK (type IN ('BUY', 'SELL')) NOT NULL,
    units FLOAT NOT NULL,
    price FLOAT NOT NULL,                    -- Auto-fetched from Prices table
    date DATE NOT NULL
);

-- Sample Data (for testing)
INSERT INTO users (name, email, password) VALUES 
('Saish Ghadi', 'saish@gmail.com', '$2b$12$yN9qSdZC1qz3EIKn5j7Z7ebnE6Ykkp8c5ZLVuKMc5X7LMEq5M0Uzu'); 
-- (hashed password = "123456")

INSERT INTO prices (symbol, current_price) VALUES
('TCS', 3400),
('INFY', 1520),
('HDFC', 1650),
('RELIANCE', 2470);

INSERT INTO transactions (user_id, symbol, type, units, price, date) VALUES
(1, 'TCS', 'BUY', 5, 3400, '2025-05-10'),
(1, 'INFY', 'BUY', 10, 1520, '2025-06-12'),
(1, 'HDFC', 'BUY', 8, 1650, '2025-07-15');
