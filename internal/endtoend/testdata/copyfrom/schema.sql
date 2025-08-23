CREATE TABLE authors (
  id         SERIAL PRIMARY KEY,
  name       text   NOT NULL,
  bio        text   NOT NULL
);

CREATE TABLE users (
  id         SERIAL PRIMARY KEY,
  email      text   NOT NULL,
  name       text   NOT NULL,
  bio        text,
  age        int,
  active     boolean DEFAULT true,
  created_at timestamp NOT NULL DEFAULT NOW()
);