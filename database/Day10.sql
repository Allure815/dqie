---Blocking
SELECT pid, state, query
FROM pg_stat_activity
WHERE datname = current_database();

---Long running

SELECT 
    pid,
    now() - query_start AS duration,
    state,
    query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;

BEGIN;
UPDATE test_users
SET name = 'LOCKED'
WHERE id = 1;
COMMIT;

--------------RUN this in a mew window before above line commit to chack the blocking 
UPDATE test_users
SET name = 'TRYING'
WHERE id = 1;


SELECT 
    pid,
    state,
    wait_event,
    query
FROM pg_stat_activity
WHERE wait_event IS NOT NULL;


SELECT 
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
ON blocking.pid = ANY(pg_blocking_pids(blocked.pid));
