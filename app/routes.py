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

'''URL template: http://127.0.0.1:5000/endpoint?arg1=1&finishdate=2019-03-12 21:11:10'''
@app.route('/addtask', methods=['POST'])
def inserttask():
    respid = int(request.args.get('respid'))
    projid = int(request.args.get('projid'))
    try:
        finishdate = request.args.get('finishdate')
        sqlconn = MySqlConn()
        testquery = sqlconn.run('INSERT INTO task (respid, projid, finishdate) VALUES (%d, %d, "%s");' %(respid, projid, finishdate))
    except:
        finishdate = 'CURRENT_TIMESTAMP'
        sqlconn = MySqlConn()
        testquery = sqlconn.run('INSERT INTO task (respid, projid, finishdate) VALUES (%d, %d, %s);' %(respid, projid, finishdate))

    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)


'''
SELECT ROUTES
URL template: http://127.0.0.1:5000/endpoint?arg1=1&arg2=hello
'''
@app.route('/emp')
def selectemp():
    sqlconn = MySqlConn()
    testquery = sqlconn.run('SELECT * FROM employee;')
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/proj')
def selectproj():
    sqlconn = MySqlConn()
    testquery = sqlconn.run('SELECT * FROM project;')
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/task')
def selecttask():
    sqlconn = MySqlConn()
    testquery = sqlconn.run('SELECT * FROM task;')
    sqlconn.connection.close()
    return jsonify(testquery)

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
    testquery = sqlconn.run('SELECT COUNT(*) FROM works WHERE empid=%d;' %(empid))
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/projofcatname')
def selectprojofcatname():
    catname = request.args.get('catname')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('''
    SELECT project.projname
    FROM project
    INNER JOIN category ON project.catid=category.id
    WHERE category.catname="%s";'''%(catname))
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/countprojofcatname')
def selectcountprojofcatname():
    sqlconn = MySqlConn()
    testquery = sqlconn.run('''
    SELECT COUNT(*), category.catname
    FROM category
    INNER JOIN project ON category.id=project.catid
    GROUP BY category.catname;''')
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/weektasks')
def selectweektasks():
    sqlconn = MySqlConn()
    testquery = sqlconn.run('''
    SELECT TIMESTAMPDIFF(MINUTE, task.finishdate, CURRENT_TIMESTAMP) AS elapsedtime, employee.empname
    FROM task
    INNER JOIN employee ON task.respid=employee.id
    HAVING elapsedtime<10080;''')
    sqlconn.connection.close()
    return jsonify(testquery)

@app.route('/empweektasks')
def selectempweektasks():
    empid = int(request.args.get('empid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('''
    SELECT TIMESTAMPDIFF(MINUTE, task.finishdate, CURRENT_TIMESTAMP) AS elapsedtime, employee.empname
    FROM task
    INNER JOIN employee ON task.respid=employee.id
    WHERE employee.id=%d
    HAVING elapsedtime<10080;'''%(empid))
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

@app.route('/deletetask', methods=['POST'])
def deletetask():
    taskid = int(request.args.get('taskid'))

    sqlconn = MySqlConn()
    testquery = sqlconn.run('DELETE FROM task WHERE task.id=%d;' %(taskid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)


'''
UPDATE ROUTES
URL template: http://127.0.0.1:5000/endpoint?arg1=1&arg2=hello
'''

@app.route('/updateemp', methods=['POST'])
def updateemp():
    empid = int(request.args.get('empid'))
    newempname = request.args.get('newempname')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('UPDATE employee SET employee.empname="%s" WHERE employee.id=%d;' %(newempname, empid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)



@app.route('/updateproj', methods=['POST'])
def updateproj():
    projid = int(request.args.get('projid'))
    newprojname = request.args.get('newprojname')

    sqlconn = MySqlConn()
    testquery = sqlconn.run('UPDATE project SET project.projname="%s" WHERE project.id=%d;' %(newprojname, projid))
    sqlconn.connection.commit()
    sqlconn.connection.close()
    return jsonify(testquery)



