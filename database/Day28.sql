----#Incidents

CREATE TABLE IF NOT EXISTS incidents (
    incident_id SERIAL PRIMARY KEY,
    pid INT,
    query TEXT,
    duration INTERVAL,
    issue_type TEXT,
    risk_score INT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-----Alerts
CREATE TABLE IF NOT EXISTS alerts (
    alert_id SERIAL PRIMARY KEY,
    message TEXT,
    alert_type TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP
);

----Action Table
CREATE TABLE action_logs (
    action_id SERIAL PRIMARY KEY,
    action_type TEXT,
    target_pid INT,
    status TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO incidents (pid, query, duration, issue_type, risk_score)
VALUES
(1111, 'SELECT * FROM users', '15 seconds', 'SLOW', 60),
(2222, 'SELECT * FROM orders', '40 seconds', 'SLOW', 85),
(3333, 'UPDATE users SET name = ''A''', '5 seconds', 'NORMAL', 20);