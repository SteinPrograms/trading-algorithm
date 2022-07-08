CREATE DATABASE trading_db
CREATE TABLE positions (
    position_id int,
    time varchar(255),
    symbol varchar(255),
    yield varchar(255),
    wallet_value varchar(255) 
);

CREATE TABLE server (
    id int,
    current_status varchar(255),
    total_yield varchar(255),
    running_time varchar(255),
);

CREATE TABLE target (
    id int,
    symbol varchar(255),
    buy_price varchar(255),
    sell_price varchar(255),
);