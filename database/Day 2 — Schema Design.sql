CREATE TABLE sessions (
    session_id SERIAL PRIMARY KEY,
    user_name TEXT,
    status TEXT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE queries (
    query_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES sessions(session_id),
    query_text TEXT,
    execution_time INT
);

CREATE TABLE incidents (
    incident_id SERIAL PRIMARY KEY,
    query_id INT REFERENCES queries(query_id),
    issue_type TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO sessions (user_name, status)
VALUES 
('user1', 'active'),
('user2', 'idle');

INSERT INTO queries (session_id, query_text, execution_time)
VALUES 
(1, 'SELECT * FROM test_users', 2),
(1, 'SELECT * FROM test_users WHERE id = 1', 1),
(2, 'UPDATE test_users SET name = ''X'' WHERE id = 2', 5);

--Session 1 ran this query and it took 2 seconds
--Session 2 ran this query and it took 5 seconds

INSERT INTO incidents (query_id, issue_type)
VALUES 
(3, 'slow query'),
(3, 'high CPU usage');

SELECT * FROM sessions;
SELECT * FROM queries;
SELECT * FROM incidents;