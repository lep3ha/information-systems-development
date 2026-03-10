INSERT INTO users (username, first_name, password_hash) VALUES
    ('alex', 'Александр', 'daa6ac887c3b88f5784a1439d11ad6071114fcc0a8e021992366f0a18010092d'),
    ('maria', 'Мария', 'ab33f3617d384bc9164095c1c850e260388661766347d33904d132bf77f72e58');

INSERT INTO user_permission (user_id, permission, role) VALUES
    ((SELECT id FROM users WHERE username = 'alex'), 'catalog', 'viewer'),
    ((SELECT id FROM users WHERE username = 'alex'), 'suppliers', 'viewer'),
    ((SELECT id FROM users WHERE username = 'alex'), 'invoices', 'viewer'),
    ((SELECT id FROM users WHERE username = 'alex'), 'reports', 'creator'),
    ((SELECT id FROM users WHERE username = 'maria'), 'catalog', 'viewer'),
    ((SELECT id FROM users WHERE username = 'maria'), 'suppliers', 'viewer'),
    ((SELECT id FROM users WHERE username = 'maria'), 'invoices', 'viewer');

INSERT INTO user_permission (user_id, permission, role) VALUES
    ((select id from users where username = 'alex'), 'monitoring', 'viewer'),
    ((select id from users where username = 'maria'), 'monitoring', 'viewer');


INSERT INTO users (username, first_name, second_name, password_hash) VALUES
    ('ivan', 'Иван', 'Иванов', 'a7c3fce0af38fcb83c2f6adfa53ab220e9b1d739e2208a665ffa54267bbc8781'),
    ('olga', 'Ольга', 'Петрова', 'a7c3fce0af38fcb83c2f6adfa53ab220e9b1d739e2208a665ffa54267bbc8781');


