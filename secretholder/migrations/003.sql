CREATE TABLE IF NOT EXISTS TEAM_USER_PERMISSIONS (
    user_id int not null,
    team_id int not null,
    foreign key (user_id) references users(id),
    foreign key (team_id) references team(id),
    unique (user_id, team_id)
);
