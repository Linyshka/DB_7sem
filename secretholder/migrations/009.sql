alter table team drop constraint team_name_key;
alter table team add unique (owner, name);
