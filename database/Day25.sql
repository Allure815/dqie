CREATE TABLE incidents (
    incident_id SERIAL PRIMARY KEY,
    pid INT,
    query TEXT,
    duration INTERVAL,
    issue_type TEXT,
    risk_score INT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alerts (
    alert_id SERIAL PRIMARY KEY,
    message TEXT,
    alert_type TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP
);


SELECT * FROM incidents;
SELECT * FROM alerts;

INSERT INTO incidents (pid, query, duration, issue_type, risk_score)
VALUES
(101, 'SELECT * FROM users', '10 seconds', 'SLOW', 70),
(102, 'SELECT * FROM orders', '20 seconds', 'SLOW', 85),
(103, 'UPDATE users SET name = ''A''', '2 seconds', 'NORMAL', 20);