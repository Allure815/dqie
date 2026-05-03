SELECT * FROM queries
ORDER BY execution_time DESC
LIMIT 10;

SELECT COUNT(*) 
FROM queries
WHERE execution_time = 10;