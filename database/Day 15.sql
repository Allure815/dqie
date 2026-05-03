
----COUNT ISSUE TYPES
SELECT issue_type, COUNT(*) AS total
FROM incidents
GROUP BY issue_type
ORDER BY total DESC;

----COUNT ROOT CAUSES

SELECT root_cause, COUNT(*) AS total
FROM incidents
GROUP BY root_cause
ORDER BY total DESC;

----MOST COMMON RECOMMENDATION
SELECT recommendation, COUNT(*) AS total
FROM incidents
GROUP BY recommendation
ORDER BY total DESC;

---DAILY INCIDENT COUNT (BASIC TREND)
SELECT DATE(created_time) AS day, COUNT(*) AS total
FROM incidents
GROUP BY day
ORDER BY day;




----MOST PROBLEMATIC QUERY
SELECT query, COUNT(*) AS total
FROM incidents
GROUP BY query
ORDER BY total DESC
LIMIT 5;

----High risk incident count

SELECT COUNT(*) AS high_risk_count
FROM incidents
WHERE risk_score >= 80;