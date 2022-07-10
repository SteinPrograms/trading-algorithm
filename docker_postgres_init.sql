CREATE TABLE positions (
    position_id SERIAL PRIMARY KEY,
    time VARCHAR (255) NOT NULL,
    symbol VARCHAR (255) NOT NULL,
    yield VARCHAR (255) NOT NULL,
    wallet_value VARCHAR (255) NOT NULL
);

CREATE TABLE server (
    id INT PRIMARY KEY NOT NULL,
    current_status VARCHAR (255) NOT NULL,
    total_yield VARCHAR (255) NOT NULL,
    running_time VARCHAR (255) NOT NULL
);

CREATE TABLE target 
(
    id INT PRIMARY KEY NOT NULL ,
    symbol VARCHAR (255) NOT NULL,
    buy_price VARCHAR (255) NOT NULL,
    sell_price VARCHAR (255) NOT NULL
);