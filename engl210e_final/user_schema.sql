drop table if exists Users;

CREATE TABLE Users(
    id integer primary key,
    username varchar(255),
    password varchar(255)
);