drop table if exists Tokens;
drop table if exists Audit;

CREATE TABLE Tokens(
    id integer primary key,
    token varchar(255)
);

CREATE TABLE Audit(
    id integer primary key,
    token_id integer,
    action varchar(255),
    timestamp datetime default CURRENT_TIMESTAMP, 
    foreign key (token_id) references Tokens(id)
);
