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
    direction varchar(100) not null,
    user_info text         not null,
    course    varchar(100) not null,
    sex       varchar(100) not null
);

create unique index if not exists users_mail_uindex
	on users (email);

create unique index if not exists users_t_user_id_uindex
	on users (t_user_id);

create table if not exists waiting_companions
(
    id integer default nextval('waiting_companions_id_seq'::regclass) not null
        constraint waiting_companions_pk
            primary key,
    t_user_id  bigint not null
        constraint waiting_companions_users_id_fk
            references users,
    time timestamp not null,
    criterion varchar(100) not null,
    status bigint
);

create table if not exists meetings
(
    waiting_id integer                                                 not null
        constraint meetings_waiting_companions_id_fk
            references waiting_companions,
    t_user_id  bigint                                                  not null
        constraint meeting_users_t_user_id_fk
            references users,
    time       timestamp default now()                                 not null,
    id         integer   default nextval('meetings_id_seq'::regclass) not null,
    constraint meeting_pk
        primary key (id, t_user_id)
);


create table if not exists feedbacks
(
    id                    integer default nextval('feedback_id_seq'::regclass) not null
        constraint feedback_pk
            primary key,
    t_user_id             bigint                                               not null
        constraint feedback_users_id_fk
            references users,
    waiting_id            integer                                              not null
        constraint feedback_meetings_id_fk
            references waiting_companions,
    is_meeting_took_place boolean                                              not null,
    rating                smallint,
    cancellation_reason   text
);
