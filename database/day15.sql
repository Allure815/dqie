SELECT 
CASE
    WHEN COUNT(*) FILTER (WHERE issue_type = 'BLOCKED') >
         COUNT(*) FILTER (WHERE issue_type = 'SLOW')
    THEN 'Most issues are BLOCKED queries'

    WHEN COUNT(*) FILTER (WHERE issue_type = 'SLOW') >
         COUNT(*) FILTER (WHERE issue_type = 'BLOCKED')
    THEN 'Most issues are SLOW queries'

    ELSE 'System has balanced or minimal issues'
END AS summary
FROM incidents;


----High risk summary