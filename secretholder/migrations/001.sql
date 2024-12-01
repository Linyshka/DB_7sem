-- Active: 1731877116832@@127.0.0.1@5432@pwd_manager
CREATE TABLE IF NOT EXISTS users (
    id serial primary key,
    username varchar(100) not null unique,
    is_admin boolean default false
);
