CREATE TABLE positions (
    position_id SERIAL PRIMARY KEY,
    time VARCHAR (255) NOT NULL,
    symbol VARCHAR (255) NOT NULL,
    yield REAL NOT NULL,
    wallet_value REAL NOT NULL
);

CREATE TABLE server (
    id SERIAL PRIMARY KEY,
    current_status VARCHAR (255) NOT NULL,
    total_yield REAL NOT NULL,
    running_time VARCHAR (255) NOT NULL,
    symbol VARCHAR (255) NOT NULL,
    current_position_time VARCHAR (255),
    current_price REAL NOT NULL,
    open_price REAL,
    current_yield REAL
);

CREATE TABLE target 
(
    id SERIAL PRIMARY KEY,
    symbol VARCHAR (255) NOT NULL,
    buy_price REAL NOT NULL,
    sell_price REAL NOT NULL
);