-- name: CreateAuthors :copyfrom
INSERT INTO authors (name, bio) VALUES ($1, $2);

-- name: CreateAuthor :one
INSERT INTO authors (name, bio) VALUES ($1, $2) RETURNING *;

-- name: CreateAuthorsNamed :copyfrom
INSERT INTO authors (name, bio) VALUES (@name, @bio);

-- name: CreateUser :one
INSERT INTO users (email, name) VALUES (@email, @name) RETURNING *;

-- name: CreateUsersBatch :copyfrom
INSERT INTO users (email, name) VALUES (@email, @name);

-- name: CreateUsersWithDetails :copyfrom
INSERT INTO users (email, name, bio, age, active) VALUES ($1, $2, $3, $4, $5);