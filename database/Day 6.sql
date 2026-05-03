SELECT pid, state, query
FROM pg_stat_activity
WHERE datname = current_database();


SELECT pid, state, query
FROM pg_stat_activity
WHERE state = 'active'    ---Show only currently running queries
AND datname = current_database();


----Long running queries

SELECT pid,
now() - query_start AS duration,
query
FROM pg_stat_activity
WHERE state = 'active'
AND datname = current_database();


-----Idle Sessions

SELECT pid, state, query
FROM pg_stat_activity
WHERE state = 'idle'
AND datname = current_database();

---Blocked queries

SELECT pid, state, query
FROM pg_stat_activity
WHERE wait_event IS NOT NULL
AND datname = current_database();