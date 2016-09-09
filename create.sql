use patient_db;


create table patient_records (
	ID int NOT NULL auto_increment,
	first_name varchar(50) NOT NULL,
	last_name varchar(50) NOT NULL,
    MSN BIGINT NOT NULL,
    DOB DATE NOT NULL,
    home_phone varchar(20),
    mobile_phone varchar(20),
    email_addr varchar(50),
    rule INT,
    sched INT,
    date_time DATETIME NOT NULL,
    meds varchar(50),
    text_ varchar(50),
    email varchar(50),
    phone varchar(50),
    language_ varchar(50),
    PRIMARY KEY (ID)
    );
    
show columns from patient_records;

select * from patient_records where first_name = "Jelani";

alter table patient_records drop language;
alter table patient_records add language_ varchar(25) after phone;

UPDATE patient_records SET
last_name = "Denis",
MSN = "1029384756",
DOB = "1996-02-23",
date_time = "2016-09-09 15:30:00",
language_ = "english"
WHERE id = 1;

insert into patient_records (first_name, last_name, MSN, DOB, date_time, language_)
VALUES ("Jelani", "Denis", "1029384756", "1996-02-23", "2016-09-09 15:30:00", "english")



