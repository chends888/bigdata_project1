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

import app
client = app.app.test_client()
empname = 'Joy'
v = client.post('/addemp?empname=%s'%(empname))

vv = client.get('/emp')
print(vv, v)