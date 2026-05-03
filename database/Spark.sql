CREATE TABLE IF NOT EXISTS query_history (
    query TEXT PRIMARY KEY,
    avg_duration FLOAT,
    execution_count INT,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);