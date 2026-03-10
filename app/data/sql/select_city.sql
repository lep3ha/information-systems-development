SELECT DISTINCT city 
FROM supplier 
WHERE city IS NOT NULL AND city != ''
ORDER BY city;