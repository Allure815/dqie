
CREATE TABLE IF NOT EXISTS action_logs (
    log_id SERIAL PRIMARY KEY,
    action_type TEXT,
    target_pid INT,
    status TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);