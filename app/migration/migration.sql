-- change set 1
ALTER TABLE users ADD COLUMN IF NOT EXISTS ban BOOL DEFAULT FALSE NOT NULL;

--change set 2
-- auto-generated definition
create table if not exists visitors
(
    t_user_id bigint    not null
        constraint visitors_pk
            primary key,
    time      timestamp not null
);

