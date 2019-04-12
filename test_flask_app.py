import os
import tempfile

import pytest

# import sys
# sys.path.insert(0, '/path/to/application/app/folder')
import app

import pymysql


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


def test_emp(setup_db):
    client, con = setup_db
    empname = 'Joy'
    v = client.post('/addemp?empname="%s"'%(empname))
    vv = client.get('http://127.0.0.1:5000/emp')
    print(vv)
    assert vv.data == b'1'


def test_index(setup_db):
    client, con = setup_db
    v = client.get('/')
    assert v.data == b'0'
