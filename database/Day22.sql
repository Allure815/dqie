CREATE TABLE IF NOT EXISTS alerts (
    alert_id SERIAL PRIMARY KEY,
    message TEXT,
    alert_type TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);