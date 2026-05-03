--Intelligent Query 
SELECT 
    pid,
    now() - query_start AS duration,
    wait_event,
    query,
---STEP 1 :issue type
    CASE 
        WHEN wait_event IS NOT NULL THEN 'BLOCKED'
        WHEN now() - query_start > interval '5 seconds' THEN 'SLOW'
        ELSE 'NORMAL'
    END AS issue_type,
---Step 2 : i
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
	