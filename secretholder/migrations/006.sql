CREATE TABLE IF NOT EXISTS SECRET_GROUP_USER_PERMISSIONS (
    user_id int not null,
    secret_group_id int not null,
    foreign key (user_id) references users(id),
    foreign key (secret_group_id) references secret_group(id),
    unique (user_id, secret_group_id)
);
