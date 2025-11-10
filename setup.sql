-- Create Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    symbol VARCHAR(50) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('BUY', 'SELL')) NOT NULL,
    units FLOAT NOT NULL,
    price FLOAT NOT NULL,
    date DATE NOT NULL
);

-- Create Prices table
CREATE TABLE prices (
    symbol VARCHAR(50) PRIMARY KEY,
    current_price FLOAT NOT NULL
);

-- Sample Data
INSERT INTO users (name, email) VALUES 
('Saish Ghadi', 'saish@gmail.com');

INSERT INTO prices (symbol, current_price) VALUES
('TCS', 3400),
('INFY', 1500),
('RELIANCE', 2600);

INSERT INTO transactions (user_id, symbol, type, units, price, date) VALUES
(1, 'TCS', 'BUY', 5, 3200, '2025-05-10'),
(1, 'INFY', 'BUY', 10, 1450, '2025-06-12');
