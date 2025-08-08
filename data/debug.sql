SELECT * 
FROM t_price_list tpl
JOIN t_power tp ON tp.p_id = tpl.p_id 
JOIN t_item ts ON ts.i_id = tpl.i_id
WHERE tp.p_id = (
    SELECT p_id 
    FROM t_power 
    WHERE p_power <= 200000 
    ORDER BY p_power DESC 
    LIMIT 1
)
AND tpl.i_id IN (
    'd9b60ed6e1cf4c66a15d7b4e18bcb77e', 
    '15a9b1d812944551b1edbab6bff18037', 
    '9c79931996b141f8b11eb4079b56b52c'
);

psql -U username -d nathaniel_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"