SELECT DISTINCT query_text FROM queries; ------DISTINCT=uNIQUE VALUES NOT DUPLICATE

INSERT INTO queries (session_id,query_text, execution_time)
VALUES 
(1,'SELECT * FROM test_users',2),
(1,'SELECT * FROM test_users WHERE id =1',1),
(2,'INSERT INTO test_users(name) VALUES (''A'')',3),
(2,'INSERT INTO test_users(name) VALUES (''B'')',2),
(1,'UPDATE test_users SET anme =''X'' WHERE id=1',5),
(1,'UPDATE test_users SET anme =''Y'' WHERE id=2',6),
(2,'DELETE FROM test_users WHERE id=3',4),
(2,'DELETE FROM test_users WHERE id=4',5);

---Classification
SELECT 
    query_text,
	
	CASE 
		WHEN query_text LIKE 'SELECT%' THEN 'SELECT'
     	WHEN query_text LIKE 'INSERT%' THEN 'INSERT'
	 	WHEN query_text LIKE 'DELETE%' THEN 'DELETE'
	 	WHEN query_text LIKE 'UPDATE%' THEN 'UPDATE'
	 	ELSE 'OTHER'
	END AS query_type
FROM queries;


---COUNT per type

SELECT 
	
	CASE 
		WHEN query_text LIKE 'SELECT%' THEN 'SELECT'
     	WHEN query_text LIKE 'INSERT%' THEN 'INSERT'
	 	WHEN query_text LIKE 'DELETE%' THEN 'DELETE'
	 	WHEN query_text LIKE 'UPDATE%' THEN 'UPDATE'
	 	ELSE 'OTHER'
	END AS query_type,
	COUNT (*) AS total_queries
FROM queries

GROUP BY query_type
order by total_queries DESC;


----Combine

SELECT 
	query_text,
	CASE 
		WHEN query_text LIKE 'SELECT%' THEN 'SELECT'
     	WHEN query_text LIKE 'INSERT%' THEN 'INSERT'
	 	WHEN query_text LIKE 'DELETE%' THEN 'DELETE'
	 	WHEN query_text LIKE 'UPDATE%' THEN 'UPDATE'
	 	ELSE 'OTHER'
	END AS query_type,
	COUNT (*) AS execution_count
FROM queries

GROUP BY query_text
order by execution_count DESC;


----FILTER THE RISKY
SELECT 
	query_text,
	CASE 
		WHEN query_text LIKE 'SELECT%' THEN 'SELECT'
     	WHEN query_text LIKE 'INSERT%' THEN 'INSERT'
	 	WHEN query_text LIKE 'DELETE%' THEN 'DELETE'
	 	WHEN query_text LIKE 'UPDATE%' THEN 'UPDATE'
	 	ELSE 'OTHER'
	END AS query_type,
	COUNT (*) AS execution_count
FROM queries

GROUP BY query_text
HAVING COUNT(*) > 50
order by execution_count DESC;


