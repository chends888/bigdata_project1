import os
import tempfile

import pytest

import sys
sys.path.append('../')
# sys.path.insert(0, '/path/to/application/app/folder')
import app

import pymysql
import json


@pytest.fixture
def setup_db():
    client = app.app.test_client()

    con = pymysql.connect('localhost', user='chends', password='8888', db='mysql')
    with con.cursor() as cur:
        with open('../db/fase0/fase0.sql') as f:
            for l in f.read().split(';'):
                if l.strip() == '': continue;
                cur.execute(l)
    con.commit()
    yield client, con

'''
INSERT tests
'''
def test_insert_emp(setup_db):
    client, con = setup_db
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    with con.cursor() as cur:
        cur.execute('SELECT * FROM employee;')
        data = cur.fetchall()
    assert data[0][1] == empname

def test_insert_cat(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    with con.cursor() as cur:
        cur.execute('SELECT * FROM category;')
        data = cur.fetchall()
    assert data[0][1] == catname

def test_insert_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    catid = 1
    respid = 1
    projname = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(projname, respid, catid))
    with con.cursor() as cur:
        cur.execute('SELECT * FROM project;')
        data = cur.fetchall()
    assert data[0][1] == projname

def test_insert_work(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    catid = 1
    respid = 1
    projname = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(projname, respid, catid))
    empid = 1
    projid = 1

    client.post('/addwork?empid=%d&projid=%d'%(empid, projid))
    with con.cursor() as cur:
        cur.execute('SELECT * FROM works;')
        data = cur.fetchall()
    print(data)
    assert data[0][0] == empid
    assert data[0][1] == projid


'''
SELECT tests
'''
def test_sel_emp(setup_db):
    client, con = setup_db
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    data = client.get('/emp')
    data = json.loads(data.data)
    assert data[0][1] == empname

def test_sel_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    projname = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(projname, 1, 1))

    data = client.get('/proj')
    data = json.loads(data.data)
    assert data[0][1] == projname

def test_sel_proj_cat(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    catname = 'Design'
    post = client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    proj2name = 'Design project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj2name, 1, 2))

    data = client.get('/projofcat?catid=%d'%(2))
    data = json.loads(data.data)
    assert data[0][1] == proj2name
    assert len(data) == 1

def test_sel_emp_on_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    emp2name = 'Joe'
    client.post('/addemp?empname=%s'%(emp2name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    client.post('/addwork?empid=%d&projid=%d'%(1, 1))

    data = client.get('/emponproj?projid=%d'%(1))
    data = json.loads(data.data)
    assert data[0][1] == emp1name
    assert len(data) == 1

def test_sel_proj_emp(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    proj2name = 'Coding project 2'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    client.post('/addwork?empid=%d&projid=%d'%(1, 1))

    data = client.get('/projofemp?empid=%d'%(1))
    data = json.loads(data.data)
    assert data[0][1] == proj1name
    assert len(data) == 1

def test_sel_count_proj_resp(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    emp2name = 'Joe'
    client.post('/addemp?empname=%s'%(emp2name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    proj2name = 'Coding project 2'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 2, 1))
    client.post('/addwork?empid=%d&projid=%d'%(1, 1))

    data = client.get('/projofresp?respid=%d'%(1))
    data = json.loads(data.data)
    assert data[0][0] == 1
    assert len(data) == 1

def test_sel_count_proj_emp(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    emp2name = 'Joe'
    client.post('/addemp?empname=%s'%(emp2name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    proj2name = 'Coding project 2'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 2, 1))
    client.post('/addwork?empid=%d&projid=%d'%(1, 1))
    client.post('/addwork?empid=%d&projid=%d'%(2, 2))

    data = client.get('/countprojofemp?empid=%d'%(1))
    data = json.loads(data.data)
    assert data[0][0] == 1
    assert len(data) == 1


'''
DELETE tests
'''
def test_del_work(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    emp2name = 'Joe'
    client.post('/addemp?empname=%s'%(emp2name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    client.post('/addwork?empid=%d&projid=%d'%(1, 1))
    client.post('/addwork?empid=%d&projid=%d'%(2, 1))

    client.post('/deletework?empid=%d&projid=%d'%(1, 1))
    data = client.get('/emponproj?projid=%d'%(1))
    data = json.loads(data.data)
    assert data[0][1] == emp2name
    assert len(data) == 1

def test_del_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    proj2name = 'Coding project 2'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj2name, 1, 1))

    client.post('/deleteproj?projid=%d'%(1))
    data = client.get('/proj')
    data = json.loads(data.data)
    assert data[0][1] == proj2name
    assert len(data) == 1

def test_del_emp(setup_db):
    client, con = setup_db
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    emp2name = 'Joe'
    client.post('/addemp?empname=%s'%(emp2name))

    client.post('/deleteemp?empid=%d'%(1))
    data = client.get('/emp')
    data = json.loads(data.data)
    assert data[0][1] == emp2name
    assert len(data) == 1


'''
UPDATE tests
'''
def test_upd_emp(setup_db):
    client, con = setup_db
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    newemp1name = 'Jessie'

    client.post('/updateemp?newempname=%s&empid=%d'%(newemp1name, 1))
    data = client.get('/emp')
    data = json.loads(data.data)
    assert data[0][1] == newemp1name
    assert len(data) == 1

def test_upd_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))

    newprojname = 'New Coding project 1'

    client.post('/updateproj?newprojname=%s&projid=%d'%(newprojname, 1))
    data = client.get('/proj')
    data = json.loads(data.data)
    assert data[0][1] == newprojname
    assert len(data) == 1




