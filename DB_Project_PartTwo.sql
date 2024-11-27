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
NumberOfIssues VARCHAR(255) NOT NULL,
StartDate DATE NOT NULL,
EndDate DATE NOT NULL,
Price DECIMAL(10,2) NOT NULL,
Frequency VARCHAR(45),
SubId INT NOT NULL,
Customer_id INT NOT NULL,
PRIMARY KEY (MagId),
FOREIGN KEY (SubId)  REFERENCES subscriptions(SubId) ON DELETE CASCADE,
FOREIGN KEY (Customer_id) REFERENCES customer(IdNo) ON DELETE CASCADE);

CREATE TABLE newspaper (
NewsId INT NOT NULL auto_increment,
NumberOfMonths INT NOT NULL,
StartDate date NOT NULL,
EndDate DATE NOT NULL,
Price DECIMAL(10,2) NOT NULL,
Frequency VARCHAR(45),
SubId INT NOT NULL,
Customer_id INT NOT NULL,
PRIMARY KEY (NewsId),
FOREIGN KEY (SubId) REFERENCES subscriptions(SubId) ON DELETE CASCADE,
FOREIGN KEY (Customer_id) REFERENCES customer(IdNo) ON DELETE CASCADE);

CREATE TABLE publications (
PubName VARCHAR(255) NOT NULL PRIMARY KEY,
PubType VARCHAR(45),
Frequency VARCHAR(45)
);