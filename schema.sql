CREATE TABLE Tokens(
    ID integer primary key,
    TOKEN varchar(255)
);

CREATE TABLE Audit(
    ID integer primary key,
    TOKEN varchar(255),
    ACTION varchar(255),
    Timestamp datetime default CURRENT_TIMESTAMP 
);
