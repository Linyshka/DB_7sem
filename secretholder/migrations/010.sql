alter table secret_group_user_permissions add column permission_type varchar(15) not null default 'READ';
alter table secret_group_user_permissions add check (permission_type = 'READ' or permission_type = 'READWRITE');
