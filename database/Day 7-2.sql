SELECT pid, 
       now() - query_start AS duration, 
       query
FROM pg_stat_activity
WHERE state = 'active'
AND datname = current_database();