BEGIN;

CREATE TABLE IF NOT EXISTS internal_user (
    user_id SERIAL PRIMARY KEY,
    login VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    user_group VARCHAR(100) NOT NULL
);

INSERT INTO internal_user (login, password_hash, user_group)
VALUES ('admin', 'pbkdf2:sha256:1000000$lab2-admin-2026$ad5a15322c8d06204b45a37e71b9b39aa32a7f0e7e0476e7a05c2b5b295402f0', 'admin')
ON CONFLICT (login) DO NOTHING;

INSERT INTO internal_user (login, password_hash, user_group)
VALUES ('cashier', 'pbkdf2:sha256:1000000$lab2-cashier-2026$695b914bf814f58e01ca09995f95e1098c40251e42fd2b4a7fb2d444e8b4004f', 'cashier')
ON CONFLICT (login) DO NOTHING;

COMMIT;
