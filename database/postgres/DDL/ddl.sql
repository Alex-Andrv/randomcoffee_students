create sequence if not exists waiting_companions_id_seq
	as integer;

create sequence if not exists feedback_id_seq
	as integer;

create sequence if not exists meetings_id_seq
	as integer;

create table if not exists users
(
    t_user_id bigint       not null
        constraint users_pk
            primary key,
    user_name varchar(100) not null,
    email     varchar(100) not null,
    full_name varchar(100) not null,
    user_info text         not null,
    sex       varchar(100) not null,
    is_student boolean not null,
    is_worker boolean not null,
    role varchar(100) not null,
    ban boolean not null,
    old_user boolean not null
);

create unique index if not exists users_mail_uindex
	on users (email);

create unique index if not exists users_t_user_id_uindex
	on users (t_user_id);

create table if not exists meetings
(
    id            integer default nextval('meetings_id_seq'::regclass) not null,
    t_user_id     bigint    not null
        constraint meetings_users_t_user_id_fk
            references users,
    time_matching timestamp not null,
    constraint meetings_pk
        primary key (id, t_user_id)
);

create table if not exists waiting_companions
(
    t_user_id     bigint    not null
        constraint waiting_companions_pk
            primary key
        constraint waiting_companions_users_t_user_id_fk
            references users,
    matching_time timestamp not null
);

create table if not exists feedbacks
(
    id                  integer default nextval('feedback_id_seq'::regclass) not null
        constraint feedbacks_pk
            primary key,
    t_user_id           bigint  not null
        constraint feedbacks_users_t_user_id_fk
            references users,
    meeting_id          integer not null
        constraint feedbacks_meetings_id_fk
            references meetings,
    is_meeting_took_place boolean not null,
    rating              smallint,
    cancellation_reason text
);


create table if not exists criterion
(
    t_user_id        bigint         not null
        constraint criterion_pk
            primary key
        constraint criterion_users_t_user_id_fk
            references users,
    interests        varchar(100)[] not null,
    meeting_format   varchar(100)   not null,
    preferred_places varchar(100)[] not null
);

create table if not exists start_next_matching_algo
(
    next_matching timestamp not null
);