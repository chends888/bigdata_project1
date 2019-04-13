import os
import tempfile

import pytest

import sys
sys.path.append('../')
import app

import pymysql
import json


@pytest.fixture
def setup_db():
    client = app.app.test_client()

    con = pymysql.connect('localhost', user='chends', password='8888', db='mysql')
    with con.cursor() as cur:
        with open('../db/fase1/fase1.sql') as f:
            for l in f.read().split(';'):
                if l.strip() == '': continue;
                cur.execute(l)
    con.commit()
    yield client, con



'''
Wrong INSERT tests
'''

def test_insert_emp(setup_db):
    client, con = setup_db
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    with con.cursor() as cur:
        cur.execute('SELECT * FROM employee;')
        data = cur.fetchall()
    assert data[0][1] == 'Joe'

def test_insert_cat(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    with con.cursor() as cur:
        cur.execute('SELECT * FROM category;')
        data = cur.fetchall()
    assert data[0][0] == catname

def test_insert_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    post = client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    catid = 1
    respid = 2
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
    empid = 2
    projid = 1

    client.post('/addwork?empid=%d&projid=%d'%(empid, projid))
    with con.cursor() as cur:
        cur.execute('SELECT * FROM works;')
        data = cur.fetchall()
    print(data)
    assert data[0][0] == empid
    assert data[0][1] == projid

def test_insert_task(setup_db):
    client, con = setup_db
    catname = 'Back'
    post = client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    projname = 'Back project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(projname, 1, 1))

    client.post('/addtask?respid=%d&projid=%d'%(1, 1))
    with con.cursor() as cur:
        cur.execute('SELECT * FROM task;')
        data = cur.fetchall()
    print(data)
    assert data[0][2] == 1
    assert data[0][0] == 1


'''
Wrong DELETE tests
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

    client.post('/deletework?empid=%d&projid=%d'%(2, 1))
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

    client.post('/deleteproj?projid=%d'%(0))
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

    client.post('/deleteemp?empid=%d'%(0))
    data = client.get('/emp')
    data = json.loads(data.data)
    assert data[0][1] == emp2name
    assert len(data) == 1


'''
Wrong UPDATE tests
'''

def test_upd_emp(setup_db):
    client, con = setup_db
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    newemp1name = 'Jessie'

    client.post('/updateemp?newempname=%s&empid=%d'%(newemp1name, 1))
    data = client.get('/emp')
    data = json.loads(data.data)
    assert data[0][1] == emp1name
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
    assert data[0][1] == proj1name
    assert len(data) == 1

