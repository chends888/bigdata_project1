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
    post = client.post('/addemp')
    assert post.status_code == 400

def test_insert_cat(setup_db):
    client, con = setup_db
    post = client.post('/addcat')
    assert post.status_code == 400

def test_insert_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    catid = 1
    respid = 1
    post = client.post('/addproj?respid=%d'%(respid))
    assert post.status_code == 400


def test_insert_work(setup_db):
    client, con = setup_db
    catname = 'Coding'
    client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    catid = 1
    respid = 1
    projname = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(projname, respid, catid))
    empid = 1
    projid = 1

    post = client.post('/addwork?empid=%d'%(empid))
    assert post.status_code == 400

def test_insert_task(setup_db):
    client, con = setup_db
    catname = 'Back'
    client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    projname = 'Back project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(projname, 1, 1))

    post = client.post('/addtask?respid=%d&projid=%d'%(1, 1))
    assert post.status_code == 400


'''
Wrong DELETE tests
'''

def test_del_work(setup_db):
    client, con = setup_db
    catname = 'Coding'
    client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    emp2name = 'Joe'
    client.post('/addemp?empname=%s'%(emp2name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    client.post('/addwork?empid=%d&projid=%d'%(1, 1))
    client.post('/addwork?empid=%d&projid=%d'%(2, 1))

    post = client.post('/deletework?projid=%d'%(1))
    assert post.status_code == 400

def test_del_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))
    proj2name = 'Coding project 2'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj2name, 1, 1))

    post = client.post('/deleteproj')
    assert post.status_code == 400

def test_del_emp(setup_db):
    client, con = setup_db
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    emp2name = 'Joe'
    client.post('/addemp?empname=%s'%(emp2name))

    post = client.post('/deleteemp')
    assert post.status_code == 400


'''
Wrong UPDATE tests
'''

def test_upd_emp(setup_db):
    client, con = setup_db
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    newemp1name = 'Jessie'

    post = client.post('/updateemp?empid=%d'%(1))
    data = client.get('/emp')
    data = json.loads(data.data)
    assert post.status_code == 400

def test_upd_proj(setup_db):
    client, con = setup_db
    catname = 'Coding'
    client.post('/addcat?catname=%s'%(catname))
    emp1name = 'Joy'
    client.post('/addemp?empname=%s'%(emp1name))
    proj1name = 'Coding project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(proj1name, 1, 1))

    post = client.post('/updateproj?projid=%d'%(1))
    data = client.get('/proj')
    data = json.loads(data.data)
    assert post.status_code == 400

def test_upd_task(setup_db):
    client, con = setup_db
    catname = 'Back'
    client.post('/addcat?catname=%s'%(catname))
    empname = 'Joy'
    client.post('/addemp?empname=%s'%(empname))
    projname = 'Back project 1'
    client.post('/addproj?projname=%s&respid=%d&catid=%d'%(projname, 1, 1))

    post = client.post('/updatetask?newedescript="%s"&finished=1'%('New description'))
    assert post.status_code == 400

    post = client.post('/updatetask?taskid=%d'%(1))
    assert post.status_code == 400