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
    creationdate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX respind (respid),
    INDEX catind (catid),
    FOREIGN KEY (respid)
        REFERENCES employee (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
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
        REFERENCES employee (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (projid)
        REFERENCES project (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE task (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    descript VARCHAR(500),
    respid INT,
    projid INT NOT NULL,
    creationdate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finishdate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX respind (respid),
    INDEX projind (projid),
    FOREIGN KEY (respid)
        REFERENCES employee (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (projid)
        REFERENCES project (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);