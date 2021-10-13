INSERT INTO users (email, hashed_password, is_active, confirmation)
VALUES ('admin@admin.com','$2b$12$UKv6whbIteBbIsION9igLef5qOS6yzLn1MczUCST7X6RDn18afzZ2', TRUE, NULL),
       ('employee@employee.com', '$2b$12$zephffybu7I5BZ7Lu5lHX.ffqqG5CadkO4AL0DaSEgk6IXvKrP6Je', TRUE, NULL);

INSERT INTO roles (name, description)
VALUES ('admin', 'user has administrative rights'),
       ('employee', 'user has employee rights');

INSERT INTO user_roles (users_id, roles_id)
VALUES (1,1),
       (2,2);