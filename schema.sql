-- Drop tables
DROP TABLE IF EXISTS "notes";
DROP TABLE IF EXISTS "users";

CREATE TABLE "users" (
    "id" INTEGER,
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL,
    "first_name" TEXT NOT NULL,
    PRIMARY KEY("id")
);


CREATE TABLE "notes" (
    "id" INTEGER,
    "user_id" INTEGER,
    "data" TEXT NOT NULL,
    "timestamp" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE
);

