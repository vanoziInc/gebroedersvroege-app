INSERT INTO users (email, hashed_password, is_active, confirmation)
VALUES ('test_admin@test.com','$2b$12$UKv6whbIteBbIsION9igLef5qOS6yzLn1MczUCST7X6RDn18afzZ2', TRUE, NULL),
       ('test_werknemer@test.com', '$2b$12$X6OGY1eXztIH2rYDwyVFO.nmrPYq98kla4JmweOu4N/oMgoe3yaKK', TRUE, NULL);

INSERT INTO roles (name, description)
VALUES ('admin', 'User met admin rechten'),
       ('werknemer', 'User met algemene werknemers rechten');

INSERT INTO user_roles (users_id, roles_id)
VALUES (1,1),
       (2,2);