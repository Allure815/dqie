SELECT 
    pid,
    now() - query_start AS duration,
    wait_event,
    query,

-- Step 1: Issue Type
    CASE 
        WHEN wait_event IS NOT NULL THEN 'BLOCKED'
        WHEN now() - query_start > interval '5 seconds' THEN 'SLOW'
        ELSE 'NORMAL'
    END AS issue_type,

-- Step 2: Root Cause
    CASE 
        WHEN wait_event IS NOT NULL THEN 'LOCK WAIT'
        WHEN now() - query_start > interval '15 seconds' THEN 'VERY LONG QUERY'
        WHEN query ILIKE '%join%' THEN 'CHECK INDEX ON JOIN'
        WHEN query ILIKE '%select *%' THEN 'FULL TABLE SCAN'
        ELSE 'UNKNOWN'
    END AS root_cause,

-- Step 3: Risk Score
    CASE    
        WHEN wait_event IS NOT NULL THEN 90
        WHEN now() - query_start > interval '15 seconds' THEN 80
        WHEN now() - query_start > interval '5 seconds' THEN 60
        ELSE 20
    END AS risk_score,

-- Step 4: Recommendation
    CASE
        WHEN wait_event IS NOT NULL THEN 'CHECK BLOCKING QUERY AND TERMINATE BLOCKER'
        WHEN query ILIKE '%join%' THEN 'ADD INDEX ON JOIN COLUMNS'
        WHEN query ILIKE '%select *%' THEN 'AVOID SELECT *, USE REQUIRED COLUMNS'
        WHEN now() - query_start > interval '15 seconds' THEN 'OPTIMIZE QUERY OR CHECK EXECUTION PLAN'
        ELSE 'NO ACTION NEEDED'
    END AS recommendation

FROM pg_stat_activity
WHERE state = 'active'
ORDER BY risk_score DESC;