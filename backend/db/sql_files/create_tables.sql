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
    "weight" DOUBLE PRECISION NOT NULL,
    "first_milk" VARCHAR(255) NOT NULL,
    "birth_process" VARCHAR(255) NOT NULL,
    "twins" BOOL NOT NULL  DEFAULT False,
    "reverse" BOOL NOT NULL  DEFAULT False,
    "cesarean_section" BOOL NOT NULL  DEFAULT False,
    "embryo" BOOL NOT NULL  DEFAULT False,
    "remarks" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "cow" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "ear_number" INT,
    "necklace_number" INT,
    "necklace_number_mother" INT NOT NULL,
    "date_of_birth" DATE NOT NULL,
    "date_of_death" DATE,
    "gender" VARCHAR(255) NOT NULL,
    "breed" VARCHAR(255) NOT NULL,
    "birth_id" INT NOT NULL REFERENCES "birth" ("id") ON DELETE CASCADE
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
