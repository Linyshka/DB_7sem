CREATE TABLE IF NOT EXISTS team (
    id serial primary key,
    name varchar(100) not null unique,
    owner int not null,
    is_personal boolean not null default false,
    foreign key (owner) references users(id)
);
