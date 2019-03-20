import requests

res = requests.post('http://127.0.0.1:5000/index?arg1=Johnny')
restext = res.text
print(restext)
print(res)
def getperson():
    res = requests.get('http://127.0.0.1:5000/')
    return res.text

def test_getperson():
    assert getperson() == '[[2,"Wolfgang"],[3,"Augusto"],[4,"Maria"],[5,"Pedro"],[6,"Lucas"]]\n'
