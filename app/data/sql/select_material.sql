SELECT DISTINCT name
FROM category
WHERE name IS NOT NULL AND name != ''
ORDER BY name;