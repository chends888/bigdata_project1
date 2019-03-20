drop database if exists dharmadb;
create database dharmadb;
use dharmadb;

CREATE TABLE employee (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    empname VARCHAR(50)
);
CREATE TABLE category (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    catname VARCHAR(25)
);
CREATE TABLE project (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    projname VARCHAR(40),
    respid INT NOT NULL,
    catid INT,
    INDEX respind (respid),
    INDEX catind (catid),
    FOREIGN KEY (respid)
        REFERENCES employee (id),
	FOREIGN KEY (catid)
        REFERENCES category (id)
);
CREATE TABLE works (
    empid INT NOT NULL,
	projid INT NOT NULL,
    primary key(empid, projid),
    INDEX empind (empid),
    INDEX projind (projid),
    FOREIGN KEY (empid)
        REFERENCES employee (id),
    FOREIGN KEY (projid)
        REFERENCES project (id)
);