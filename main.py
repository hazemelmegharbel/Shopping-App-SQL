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
        if request.form.get('listButton'):
            data = request.form.get('listButton')
            session['groupID'] = data
            print(data)
            return redirect(url_for('group'))
    return render_template('groups.html')


@app.route("/groups/group", methods=['GET', 'POST'])
def group():
    if request.method == "GET":
        print("loading page")
        identifier = session.get('groupID', None)
        cur = mysql.connection.cursor()

        query = f"SELECT L.ItemName, SUM(L.Quantity) " \
                f"FROM ListItem L " \
                f"WHERE CustomerID IN " \
                f"(SELECT memberID FROM GroupMembers " \
                f"WHERE L.CustomerID = memberID AND L.ListNumber = UsesList AND GroupID = {identifier})" \
                f"GROUP BY L.ItemName;"

        cur.execute(query)
        mysql.connection.commit()
        results = cur.fetchall()

        query = f"SELECT COUNT(*) FROM GroupMembers WHERE GroupID = {identifier} AND memberID = {custID}"
        cur.execute(query)
        mysql.connection.commit()
        total = cur.fetchall()
        cur.close()
        return render_template('group.html', list=results, isMember=int(total[0][0]))
        # DISPLAY THE GROUP LIST
    elif request.method == "POST":
        # CHECK WHAT KIND OF BUTTON
        if request.form.get("JoinButton"):
            print("joining group")
            cur = mysql.connection.cursor()
            identifier = session.get('groupID', None)
            query = f"INSERT INTO `ShoppingApplication`.`GroupMembers`(groupID, memberID, UsesList) VALUES({identifier}, {custID}, {listNumber});"
            cur.execute(query)
            mysql.connection.commit()
            query = f"UPDATE Party SET numberOfMembers= numberOfMembers+1 WHERE groupID={identifier};"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('group'))
        elif request.form.get("LeaveButton"):
            print("leaving group")
            cur = mysql.connection.cursor()
            identifier = session.get('groupID', None)
            query = f"DELETE FROM `ShoppingApplication`.`GroupMembers` WHERE memberID = {custID};"
            cur.execute(query)
            mysql.connection.commit()
            query = f"UPDATE Party SET numberOfMembers= numberOfMembers-1 WHERE groupID={identifier};"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('groups'))
        return render_template('group.html')
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
        if request.form.get('listButton'):
            data = request.form.get('listButton')
            parsed = data.split()
            session['index'] = parsed[0]
            session['name'] = parsed[1]
            return redirect(url_for('items'))
        elif request.form.get('deleteButton'):
            data = request.form.get('deleteButton')
            parsed = data.split()
            session['index'] = parsed[0]
            print(parsed[0])
            cur = mysql.connection.cursor()
            query = f"DELETE FROM CustomerList WHERE CustomerID={custID} AND ListNumber={parsed[0]}"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('list'))
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
    elif request.method == "POST":
        index = session.get('index', None)
        quantity = request.form.get("quantity")
        name = request.form.get("itemName")
        if request.form.get("quantity"):
            print(quantity)
            print(index)
            print(name)
            cur = mysql.connection.cursor()
            query = f"UPDATE ListItem SET Quantity = {quantity} " \
                    f"WHERE CustomerID = {custID} AND ListNumber = {index} AND ItemName LIKE'%{name}%';"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('items'))
        elif request.form.get("deleteButton"):
            print("DELETE")
            itemName = request.form.get("deleteButton")
            print(itemName)
            cur = mysql.connection.cursor()
            query = f"DELETE FROM ListItem WHERE ItemName LIKE '%{itemName}%' AND CustomerID={custID} AND ListNumber={index}"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('items'))
        elif request.form.get("addButton"):
            print("ADDING")
            newName = request.form.get("itemNameID")
            newQuantity = request.form.get("quantityID")
            if newName is not None:
                cur = mysql.connection.cursor()
                query = f"INSERT INTO `ShoppingApplication`.`ListItem` " \
                f"(`ItemName`, `ListNumber`, `CustomerID`, `Quantity`) " \
                f"VALUES ('{newName}', '{index}', '{custID}', '{newQuantity}')"
                cur.execute(query)
                mysql.connection.commit()
                cur.close()
            else:
                # DISPLAY ERROR TO USER
                pass
            return redirect(url_for('items'))
        else:
            return redirect(url_for('items'))
    else:
        return render_template('listitems.html')

if __name__ == '__main__':
    app.run(debug=True)
