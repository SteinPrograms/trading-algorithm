CREATE TABLE positions (
    id SERIAL PRIMARY KEY NOT NULL,
    open_price REAL,
    close_price REAL,
    highest_price REAL,
    lowest_price REAL,
    current_price REAL,
    open_date TIMESTAMP,
    close_date TIMESTAMP,
    status VARCHAR (255),
    exit_mode VARCHAR (255)
);

CREATE TABLE vitals (
    id SERIAL PRIMARY KEY NOT NULL,
    status VARCHAR (255),
    total_net_return REAL,
    running_time VARCHAR (255),
    current_price REAL
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    log_level REAL NULL,
    log_levelname VARCHAR (255) NOT NULL,
    log_content VARCHAR (2048) NOT NULL,
    created_at TIMESTAMP NOT NULL
);