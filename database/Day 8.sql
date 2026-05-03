Select * from queries;

SELECT query_text,COUNT (*) as execution_count FROM queries ------Selecting query and countig the occureence and storing count in a new table named exec_coutn from queries table
GROUP BY query_text 
ORDER BY execution_count DESC;

SELECT query_text,COUNT (*) as execution_count FROM queries
GROUP BY query_text 
HAVING COUNT(*)>50
ORDER BY execution_count DESC;
