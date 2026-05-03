----Issue Summary
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

SELECT 
CASE
    WHEN COUNT(*) FILTER (WHERE risk_score >= 80) > 5
    THEN 'High number of critical issues detected'

    WHEN COUNT(*) FILTER (WHERE risk_score >= 80) > 0
    THEN 'Some critical issues detected'

    ELSE 'No critical issues, system stable'
END AS risk_summary
FROM incidents;


---Root Cause Summary

SELECT 
root_cause,
COUNT(*) AS total
FROM incidents
GROUP BY root_cause
ORDER BY total DESC
LIMIT 1;


---Convert Root Cause Summary in Sentence

SELECT 
CASE 
    WHEN root_cause = 'FULL TABLE SCAN'
    THEN 'Most issues are caused by full table scans'

    WHEN root_cause = 'LOCK WAIT'
    THEN 'Most issues are due to locking problems'

    ELSE 'Various root causes detected'
END AS root_summary
FROM (
    SELECT root_cause
    FROM incidents
    GROUP BY root_cause
    ORDER BY COUNT(*) DESC
    LIMIT 1
) sub;


---Sys Health Summary

SELECT 
CASE
    WHEN COUNT(*) FILTER (WHERE risk_score >= 80) > 5
    THEN 'System is under high stress'

    WHEN COUNT(*) FILTER (WHERE risk_score >= 60) > 5
    THEN 'System performance needs attention'

    ELSE 'System is stable'
END AS health_status
FROM incidents;


----Final Summary 

SELECT 

-- Issue Summary
CASE
    WHEN COUNT(*) FILTER (WHERE issue_type = 'BLOCKED') >
         COUNT(*) FILTER (WHERE issue_type = 'SLOW')
    THEN 'Most issues are BLOCKED queries'
    ELSE 'Most issues are SLOW queries'
END AS issue_summary,

-- Risk Summary
CASE
    WHEN COUNT(*) FILTER (WHERE risk_score >= 80) > 5
    THEN 'High number of critical issues detected'
    ELSE 'System has manageable risk levels'
END AS risk_summary

FROM incidents;
