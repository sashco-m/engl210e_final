drop table if exists Tokens;
drop table if exists Audit;

CREATE TABLE Tokens(
    id integer primary key,
    token varchar(255),
    step integer default 1 not null
);

CREATE TABLE Audit(
    id integer primary key,
    token_id integer,
    action varchar(255),
    timestamp datetime default CURRENT_TIMESTAMP, 
    foreign key (token_id) references Tokens(id)
);
