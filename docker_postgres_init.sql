CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    time VARCHAR (255) NOT NULL,
    net_return REAL NOT NULL
);

CREATE TABLE vitals (
    id SERIAL PRIMARY KEY NOT NULL,
    status VARCHAR (255),
    total_net_return REAL,
    running_time VARCHAR (255),
    current_position_time VARCHAR (255),
    current_price REAL,
    open_price REAL,
    current_yield REAL
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    log_level REAL NULL,
    log_levelname VARCHAR (255) NOT NULL,
    log_content VARCHAR (2048) NOT NULL,
    created_at TIMESTAMP NOT NULL
);