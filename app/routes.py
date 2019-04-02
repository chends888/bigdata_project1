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



@app.route('/')
def select():
    sqlconn = MySqlConn()
    testquery = sqlconn.run('SELECT * FROM employee;')
    sqlconn.connection.close()
    return jsonify(testquery)

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
    respid = request.args.get('respid')
    catid = request.args.get('catid')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('INSERT INTO project (projname, respid, catid) VALUES ("%s", %d, %d);' %(projname, respid, catid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/addwork', methods=['POST'])
def insertwork():
    empid = request.args.get('empid')
    projid = request.args.get('projid')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('INSERT INTO works (empid, projid) VALUES (%d, %d);' %(empid, projid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)





