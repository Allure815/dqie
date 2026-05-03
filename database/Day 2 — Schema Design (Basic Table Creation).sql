CREATE TABLE test_users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--CREATE TABLE → create new table
--test_users → table name
--id → unique number (auto-generated)
--name → text data
--created_at → auto time of creation

INSERT INTO test_users (name)
VALUES 
('A'),
('B'),
('C'),
('D'),
('E');

SELECT * FROM test_users;
--Read query → Plan → Execute → Return result