CREATE DATABASE magazine_newspapers;
USE magazine_newspapers;

CREATE TABLE customer (
IdNo int NOT NULL auto_increment,
FName VARCHAR(45) NOT NULL,
LName VARCHAR(45) NOT NULL,
Address VARCHAR(225) NOT NULL,
PRIMARY KEY (IdNo));

CREATE TABLE subscriptions (
SubId INT NOT NULL AUTO_INCREMENT,
SubType VARCHAR(45) NOT NULL,
Customer_id INT NOT NULL,
PRIMARY KEY (SubId), -- had to rename this from PRIMARY KEY (Subscription_Id), "Subscription_Id" does not exist at this point of the script
FOREIGN KEY (Customer_id) REFERENCES customer(IdNo) ON DELETE CASCADE);

CREATE TABLE magazine (
MagId INT NOT NULL auto_increment,
MagType VARCHAR(45) NOT NULL,
NumberOfIssues VARCHAR(255) NOT NULL,
StartDate DATE NOT NULL,
EndDate DATE NOT NULL,
Price DECIMAL(10,2) NOT NULL,
SubId INT NOT NULL,
Customer_id INT NOT NULL,
PRIMARY KEY (MagId),
FOREIGN KEY (SubId)  REFERENCES subscriptions(SubId) ON DELETE CASCADE,
FOREIGN KEY (Customer_id) REFERENCES customer(IdNo) ON DELETE CASCADE);

CREATE TABLE newspaper (
NewsId INT NOT NULL auto_increment,
NewsType VARCHAR(45) NOT NULL,
NumberOfMonths INT NOT NULL,
StartDate date NOT NULL,
EndDate DATE NOT NULL,
Price DECIMAL(10,2) NOT NULL,
SubId INT NOT NULL,
Customer_id INT NOT NULL,
PRIMARY KEY (NewsId),
FOREIGN KEY (SubId) REFERENCES subscriptions(SubId) ON DELETE CASCADE,
FOREIGN KEY (Customer_id) REFERENCES customer(IdNo) ON DELETE CASCADE);

CREATE TABLE publications (
PubName VARCHAR(255) NOT NULL PRIMARY KEY,
PubType VARCHAR(45)
);

use magazine_newspapers;
ALTER TABLE `magazine_newspapers`.`magazine` 
ADD CONSTRAINT `PubName`
  FOREIGN KEY (`PubName`)
  REFERENCES `magazine_newspapers`.`publications` (`PubName`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
insert into publications (PubName, PubType) values ('Joe Rogan', 'Podcast');
insert into publications (PubName, PubType) values ('Talk Tuah', 'Podcast');

select * from customer;
select * from publications;
select * from subscriptions;
select * from customer where IdNo = 1;
select count(distinct Fname) + sum(if(Fname is null, 1, 0)) as count from customer;
insert into customer (LName, FName, Address) values ('jogan', 'b', 'bikini bottom');
insert into subscriptions (SubType, Customer_id) values ('Magazine', 1);
  

