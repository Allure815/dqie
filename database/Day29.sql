



-- INCIDENTS
CREATE TABLE IF NOT EXISTS incidents (
    incident_id SERIAL PRIMARY KEY,
    pid INT,
    query TEXT,
    duration_seconds INT,
    issue_type TEXT,
    risk_score INT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ALERTS
CREATE TABLE IF NOT EXISTS alerts (
    alert_id SERIAL PRIMARY KEY,
    message TEXT,
    alert_type TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP
);

-- ACTION LOGS
CREATE TABLE IF NOT EXISTS action_logs (
    action_id SERIAL PRIMARY KEY,
    action_type TEXT,
    target_pid INT,
    status TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO incidents (pid, query, duration_seconds, issue_type, risk_score)
VALUES
(101, 'SELECT * FROM users', 12, 'SLOW', 60),
(202, 'SELECT * FROM orders', 45, 'SLOW', 85),
(303, 'UPDATE users SET name=''A''', 5, 'NORMAL', 20);