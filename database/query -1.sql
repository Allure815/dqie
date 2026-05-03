BEGIN;

UPDATE test_users 
SET name = 'Blocked_User'
WHERE id = 1;

COMMIT;