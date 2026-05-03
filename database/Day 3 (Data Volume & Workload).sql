INSERT INTO test_users (name)
SELECT 'User_' || generate_series(1, 10000);


--👉 generate_series(1, 10000) : Creates numbers from 1 to 10000
--👉 'User_' || number : Combines text + number

SELECT COUNT(*) FROM test_users;

SELECT * FROM test_users;

SELECT * FROM test_users WHERE id = 5000;

INSERT INTO queries (session_id, query_text, execution_time)
SELECT 
    1,
    'SELECT * FROM test_users WHERE id = ' || generate_series(1, 1000),
    (random() * 10)::int;

SELECT * FROM queries LIMIT 10;

