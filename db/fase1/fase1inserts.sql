INSERT INTO employee (empname) VALUES ("Jessie");
INSERT INTO employee (empname) VALUES ("Joe");
INSERT INTO category (catname) VALUES ("Cloud");
INSERT INTO category (catname) VALUES ("Front");
INSERT INTO project (projname, respid, catid) VALUES ("Claud proj 1", 1, 1);
INSERT INTO project (projname, respid, catid) VALUES ("Claud proj 2", 2, 1);
INSERT INTO project (projname, respid, catid) VALUES ("Front", 2, 2);
INSERT INTO works (empid, projid) VALUES (1, 1);
INSERT INTO works (empid, projid) VALUES (2, 1);
INSERT INTO works (empid, projid) VALUES (2, 2);
INSERT INTO task (projid, respid) VALUES (1, 1);

-- UPDATE task SET task.respid=1 WHERE task.id=1;
-- INSERT INTO task (projid, respid, finishdate) VALUES (1, 1, 2019-03-12 21:11:10);