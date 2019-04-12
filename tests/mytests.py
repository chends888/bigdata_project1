# import requests
# res = requests.get('http://127.0.0.1:5000/emp')
# restext = res.text
# print(restext)
# print(res)
# def getperson():
#     res = requests.get('http://127.0.0.1:5000/')
#     return res.text

# def test_getperson():
#     assert getperson() == '[[2,"Wolfgang"],[3,"Augusto"],[4,"Maria"],[5,"Pedro"],[6,"Lucas"]]\n'

import pymysql
import sys
sys.path.append('../')
import app
client = app.app.test_client()
con = pymysql.connect('localhost', user='chends', password='8888', db='mysql')
with con.cursor() as cur:
    with open('../db/fase0/fase0.sql') as f:
        for l in f.read().split(';'):
            if l.strip() == '': continue;
            cur.execute(l)
con.commit()

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
print(len(data))

# print(v.status_code)