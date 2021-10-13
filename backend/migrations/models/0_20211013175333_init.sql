-- upgrade --
CREATE TABLE IF NOT EXISTS "allowed_users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "email" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "birth" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "weight" DOUBLE PRECISION,
    "first_milk" VARCHAR(255),
    "birth_process" VARCHAR(255),
    "twins" BOOL NOT NULL  DEFAULT True,
    "reverse" BOOL NOT NULL  DEFAULT True,
    "cesarean_section" BOOL NOT NULL  DEFAULT True,
    "embryo" BOOL NOT NULL  DEFAULT True,
    "remarks" TEXT
);
CREATE TABLE IF NOT EXISTS "cow" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "ear_number" INT,
    "necklace_number" INT,
    "necklace_number_mother" INT,
    "date_of_birth" DATE,
    "date_discharched" TIMESTAMPTZ,
    "reason_discharched" VARCHAR(255),
    "gender" VARCHAR(255),
    "breed" VARCHAR(255),
    "birth_id" INT NOT NULL REFERENCES "birth" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "calve" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "mother_id" INT REFERENCES "cow" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "roles" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "email" VARCHAR(255) NOT NULL,
    "hashed_password" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "confirmation" UUID
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_roles" (
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "roles_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE
);
