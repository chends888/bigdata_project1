import pymysql
from flask import jsonify, request
import flask


#local imports
from app import app

class ConnectionHelper:
    def __init__(self, connection):
        self.connection = connection
    
    def run(self, query):
        with self.connection.cursor() as cursor:
            print('Executing query:')
            print(cursor.mogrify(query))
            cursor.execute(query)
            return cursor.fetchall()

connection_options = {
    'host': 'localhost',
    'user': 'chends',
    'password': '8888',
    'database': 'dharmadb',
}
connection = pymysql.connect(**connection_options)
db = ConnectionHelper(connection)

@app.route('/')
def index():
    testquery = db.run('SELECT * FROM person')
    return jsonify(testquery)

@app.route('/index', methods=['GET', 'POST'])
def index2():
    if flask.request.method == 'GET':
        testquery = db.run('SELECT * FROM employee')
        return jsonify(testquery)
    else:
        testquery = db.run('INSERT INTO employee (empname) VALUES ('+request.args.get('arg1')+')')
        args = request.args.get('arg1')
        return args