SELECT id, company_name, city, phone, contract_date
FROM supplier
WHERE city = %s;
