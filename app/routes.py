import pymysql
import functools
from flask import jsonify, request
import flask


#local imports
from app import app


class MySqlConn:
    def __init__(self):
        connection_options = {
            'host': 'localhost',
            'user': 'chends',
            'password': '8888',
            'database': 'dharmadb'}
        self.connection = pymysql.connect(**connection_options)

    def run(self, query, args=None):
        with self.connection.cursor() as cursor:
            print('Executing query:')
            print(cursor.mogrify(query, args))
            cursor.execute(query, args)
            return cursor.fetchall()



'''
INSERT ROUTES
URL template: http://127.0.0.1:5000/endpoint?arg1=1&arg2=hello
'''
@app.route('/addemp', methods=['POST'])
def insertemp():
    empname = request.args.get('empname')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('INSERT INTO employee (empname) VALUES ("%s");' %(empname))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/addcat', methods=['POST'])
def insertcat():
    catname = request.args.get('catname')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('INSERT INTO category (catname) VALUES ("%s");' %(catname))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/addproj', methods=['POST'])
def insertproj():
    projname = request.args.get('projname')
    respid = int(request.args.get('respid'))
    catid = int(request.args.get('catid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('INSERT INTO project (projname, respid, catid) VALUES ("%s", %d, %d);' %(projname, respid, catid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/addwork', methods=['POST'])
def insertwork():
    empid = int(request.args.get('empid'))
    projid = int(request.args.get('projid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('INSERT INTO works (empid, projid) VALUES (%d, %d);' %(empid, projid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)




'''
SELECT ROUTES
URL template: http://127.0.0.1:5000/endpoint?arg1=1&arg2=hello
'''
# @app.route('/')
# def select():
#     sqlconn = MySqlConn()
#     testquery = sqlconn.run('SELECT * FROM employee;')
#     sqlconn.connection.close()
#     return jsonify(testquery)

@app.route('/projofcat')
def selectprojofcat():
    catid = int(request.args.get('catid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('SELECT * FROM project WHERE catid=%d;' %(catid))
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/emponproj')
def selectemponproj():
    projid = int(request.args.get('projid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('''
    SELECT works.empid,employee.empname
    FROM employee,works
    WHERE works.projid=%d AND employee.id = works.empid''' %(projid))
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/projofemp')
def selectprojofemp():
    empid = int(request.args.get('empid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('''
    SELECT works.projid,project.projname
    FROM project,works
    WHERE works.empid=%d AND project.id = works.projid''' %(empid))
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/projofresp')
def selectprojofresp():
    respid = int(request.args.get('respid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('SELECT COUNT(*) FROM project WHERE respid=%d;' %(respid))
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/countprojofemp')
def selectcountprojofemp():
    empid = int(request.args.get('empid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('SELECT COUNT(*) FROM wokrs WHERE empid=%d;' %(empid))
    sqlconn.connection.close()
    return jsonify(testquery)









'''
DELETE ROUTES
URL template: http://127.0.0.1:5000/endpoint?arg1=1&arg2=hello
'''

@app.route('/deletework', methods=['POST'])
def deletework():
    empid = int(request.args.get('empid'))
    projid = int(request.args.get('projid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('DELETE FROM works WHERE empid=%d AND projid=%d;' %(empid, projid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)


@app.route('/deleteproj', methods=['POST'])
def deleteproj():
    projid = int(request.args.get('projid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('DELETE FROM project WHERE project.id=%d;' %(projid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)


@app.route('/deleteemp', methods=['POST'])
def deleteemp():
    empid = int(request.args.get('empid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('DELETE FROM employee WHERE employee.id=%d;' %(empid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)



'''
UPDATE ROUTES
URL template: http://127.0.0.1:5000/endpoint?arg1=1&arg2=hello
'''

@app.route('/updateemp', methods=['POST'])
def updateemp():
    empname = request.args.get('empname')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('UPDATE FROM employee WHERE employee.empname="%s";' %(empname))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)



@app.route('/updateproj', methods=['POST'])
def updateproj():
    projname = request.args.get('projname')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('UPDATE FROM project WHERE project.projname="%s";' %(projname))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)



