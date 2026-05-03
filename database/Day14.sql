
----Creation 
CREATE TABLE incidents (
    incident_id SERIAL PRIMARY KEY,
    pid INT,
    query TEXT,
    duration INTERVAL,
    issue_type TEXT,
    root_cause TEXT,
    risk_score INT,
    recommendation TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

----Intelligent
INSERT INTO incidents (
    pid,
    query,
    duration,
    issue_type,
    root_cause,
    risk_score,
    recommendation
)

SELECT 
    pid,
    query,
    now() - query_start AS duration,

-- Issue Type
    CASE 
        WHEN wait_event IS NOT NULL THEN 'BLOCKED'
        WHEN now() - query_start > interval '5 seconds' THEN 'SLOW'
        ELSE 'NORMAL'
    END,

-- Root Cause
    CASE 
        WHEN wait_event IS NOT NULL THEN 'LOCK WAIT'
        WHEN now() - query_start > interval '15 seconds' THEN 'VERY LONG QUERY'
        WHEN query ILIKE '%join%' THEN 'CHECK INDEX ON JOIN'
        WHEN query ILIKE '%select *%' THEN 'FULL TABLE SCAN'
        ELSE 'UNKNOWN'
    END,

-- Risk Score
    CASE    
        WHEN wait_event IS NOT NULL THEN 90
        WHEN now() - query_start > interval '15 seconds' THEN 80
        WHEN now() - query_start > interval '5 seconds' THEN 60
        ELSE 20
    END,

-- Recommendation
    CASE
        WHEN wait_event IS NOT NULL THEN 'CHECK BLOCKING QUERY AND TERMINATE BLOCKER'
        WHEN query ILIKE '%join%' THEN 'ADD INDEX ON JOIN COLUMNS'
        WHEN query ILIKE '%select *%' THEN 'AVOID SELECT *, USE REQUIRED COLUMNS'
        WHEN now() - query_start > interval '15 seconds' THEN 'OPTIMIZE QUERY OR CHECK EXECUTION PLAN'
        ELSE 'NO ACTION NEEDED'
    END

FROM pg_stat_activity
WHERE state = 'active';

----Verify 
SELECT * FROM incidents
ORDER BY created_time DESC;

--Test
SELECT pg_sleep(10);