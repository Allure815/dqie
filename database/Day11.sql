---Active queries

SELECT 
    pid,
    state,
    now() - query_start AS duration,
    wait_event,
    query
FROM pg_stat_activity
WHERE state = 'active';

---Slow Queries

SELECT 
    pid,
    now() - query_start AS duration,
    query
FROM pg_stat_activity
WHERE state = 'active'
AND now() - query_start > interval '5 seconds';

--Blocked queries
SELECT 
    pid,
    wait_event,
    query
FROM pg_stat_activity
WHERE wait_event IS NOT NULL;

---Combine

SELECT 
    pid,
    now() - query_start AS duration,
    wait_event,
    query,

    CASE 
        WHEN wait_event IS NOT NULL THEN 'BLOCKED'
        WHEN now() - query_start > interval '5 seconds' THEN 'SLOW'
        ELSE 'NORMAL'
    END AS issue_type

FROM pg_stat_activity
WHERE state = 'active';


----Adding Risk level

SELECT 
    pid,
    now() - query_start AS duration,
    wait_event,
    query,

    CASE 
        WHEN wait_event IS NOT NULL THEN 'BLOCKED'
        WHEN now() - query_start > interval '5 seconds' THEN 'SLOW'
        ELSE 'NORMAL'
    END AS issue_type,

    CASE 
        WHEN wait_event IS NOT NULL THEN 'HIGH'
        WHEN now() - query_start > interval '5 seconds' THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_level

FROM pg_stat_activity
WHERE state = 'active';


---SORT MOST CRITICAL FIRST


SELECT 
    pid,
    now() - query_start AS duration,
    wait_event,
    query,

    CASE 
        WHEN wait_event IS NOT NULL THEN 'BLOCKED'
        WHEN now() - query_start > interval '5 seconds' THEN 'SLOW'
        ELSE 'NORMAL'
    END AS issue_type,

    CASE 
        WHEN wait_event IS NOT NULL THEN 'HIGH'
        WHEN now() - query_start > interval '5 seconds' THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_level

FROM pg_stat_activity
WHERE state = 'active'
ORDER BY
	CASE	
		WHEN wait_event IS NOT NULL THEN 1
		WHEN now()-query_start > interval '5 seconds' THEN 2
		ELSE 3
	END,
	duration DESC;
	


