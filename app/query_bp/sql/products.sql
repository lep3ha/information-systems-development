SELECT p.id, p.name, c.name AS category
FROM product AS p
JOIN category AS c ON c.id = p.category_id
WHERE p.category_id = %s;
