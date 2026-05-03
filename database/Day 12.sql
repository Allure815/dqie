CREATE TABLE incidents (
    incident_id SERIAL PRIMARY KEY,
    pid INT,
    query TEXT,
    duration INTERVAL,
    issue_type TEXT,
    risk_level TEXT,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


----Insert live data(main logic)

INSERT INTO incidents (pid, query, duration, issue_type, risk_level)

SELECT 
    pid,
    query,
    now() - query_start AS duration,

--ISSUE TYPE
    CASE 
        WHEN wait_event IS NOT NULL THEN 'BLOCKED'
        WHEN now() - query_start > interval '5 seconds' THEN 'SLOW'
        ELSE 'NORMAL'
    END,
	
---risk level

    CASE 
        WHEN wait_event IS NOT NULL THEN 'HIGH'
        WHEN now() - query_start > interval '5 seconds' THEN 'MEDIUM'
        ELSE 'LOW'
    END

FROM pg_stat_activity
WHERE state = 'active';


---Verify
SELECT * FROM incidents;

---SORT

SELECT * FROM incidents ORDER BY created_time DESC;

---Risk Level
SELECT * FROM incidents WHERE risk_level = 'HIGH';
