import os

from flask import Flask, request, session, url_for
from flask import render_template

from flask_mysqldb import MySQL
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root_default1996'
app.config['MYSQL_DB'] = 'ShoppingApplication'
app.config['SECRET_KEY'] = 'KECRET_SEY'

session = {}
mysql = MySQL(app)

custID = '100000001'
listNumber = '1'

'''
    def insertCustomerList(self, ListNumber, Name, CreationDate, CustomerID):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`CustomerList` " \
                f"(`ListNumber`, `Name`, `CreationDate`, `CustomerID`) " \
                f"VALUES ('{ListNumber}', '{Name}','{CreationDate}', '{CustomerID}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()
        
        
            elif request.method == "GET" and listNumber is not None:
        cur = mysql.connection.cursor()
        query = f"SELECT L.ItemName, L.Quantity " \
                f"FROM ListItem L " \
                f"WHERE customerID = '{custID}' AND listNumber = '{listNumber}'"
        cur.execute(query)
        mysql.connection.commit()
        results = cur.fetchall()
        cur.close()
        return render_template('viewlists.html', name=results)

'''

'''
       cur = mysql.connection.cursor()
       query2 = f"SELECT Name " \
               f"FROM CustomerList " \
               f"WHERE customerID = '{custID}' AND listNumber = '{listNumber}'"
       cur.execute(query2)
       mysql.connection.commit()
       results2 = cur.fetchall()
       cur.close()
       '''


'''
    query = f"SELECT Name, CreationDate FROM CustomerList WHERE CustomerID = '{custID}'"
'''


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/groups/", methods=['GET', 'POST'])
def groups():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = f"SELECT P.groupName, G.groupID, AVG(CustomerRating)" \
                f" FROM Customer C, GroupMembers G" \
                f" INNER JOIN Party P ON P.groupID = G.groupID" \
                f" WHERE C.UserID=G.memberID " \
                f"GROUP BY G.groupID"
        cur.execute(query)
        mysql.connection.commit()
        results = cur.fetchall()
        cur.close()
        print(results)
        return render_template('groups.html', lists=results)
    elif request.method == "POST":
        data = request.form.get('listButton')
        session['groupID'] = data
        print(data)
        return redirect(url_for('group'))
    return render_template('groups.html')


@app.route("/groups/group", methods=['GET', 'POST'])
def group():
    if request.method == "GET":
        pass
        # DISPLAY THE GROUP LIST
    elif request.method == "POST":
        # RUN THE JOIN GROUP ONCLICK
        pass
    return render_template('group.html')


@app.route("/list/", methods=['GET', 'POST'])
def list():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = f"SELECT Name, CreationDate, listNumber FROM CustomerList WHERE CustomerID = '{custID}'"
        cur.execute(query)
        mysql.connection.commit()
        results = cur.fetchall()
        cur.close()
        return render_template('viewlists.html', lists=results)
    elif request.method == "POST":
        data = request.form.get('listButton')
        parsed = data.split()
        session['index'] = parsed[0]
        session['name'] = parsed[1]
        return redirect(url_for('items'))
    return render_template('viewLists.html')


@app.route("/create/", methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        data = request.form.get('nameID')
        print(data)
    return render_template('createlist.html')


@app.route("/list/items", methods=['GET', 'POST'])
def items():
    if request.method == "GET":
        index = session.get('index', None)
        name = session.get('name', None)
        print(index)
        cur = mysql.connection.cursor()
        query = f"SELECT L.ItemName, L.Quantity " \
                f"FROM ListItem L " \
                f"WHERE customerID = '{custID}' AND listNumber = '{index}'"
        cur.execute(query)
        mysql.connection.commit()
        results = cur.fetchall()
        cur.close()
        return render_template('listitems.html', list=results, Name=name)
    else:
        return render_template('listitems.html')


if __name__ == '__main__':
    app.run(debug=True)
