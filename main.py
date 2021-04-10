import os
from datetime import date
from flask import Flask, request, session, url_for
from flask import Flask, request, session, url_for, flash
from flask import render_template

from flask_mysqldb import MySQL
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector
import random

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root_default1996'
app.config['MYSQL_DB'] = 'ShoppingApplication'
app.config['SECRET_KEY'] = 'KECRET_SEY'

session = {}
mysql = MySQL(app)

session['logged_in'] = False

custID = '100000001'
listNumber = '1'


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/groups/", methods=['GET', 'POST'])
def groups():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = f"SELECT * FROM PARTY"
        cur.execute(query)
        mysql.connection.commit()
        results = cur.fetchall()
        cur.close()
        print(results)

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
        elif request.form.get('addButton'):
            groupName = request.form.get('groupNameID')
            cur = mysql.connection.cursor()
            query = f"SELECT groupID FROM Party"
            cur.execute(query)
            mysql.connection.commit()
            results = cur.fetchall()
            cur.close()
            print(results)
            groupID = max(results)[0] + 1
            print(groupID)
            if groupName:
                print(groupName)
                cur = mysql.connection.cursor()
                query = f"INSERT INTO `ShoppingApplication`.`Party`" \
                        f"(groupID, creatorID, groupName, numberOfMembers, shoppingDate) " \
                        f"VALUES ('{groupID}', '{custID}', '{groupName}', 1, null);"
                cur.execute(query)
                mysql.connection.commit()
                query = f"INSERT INTO `ShoppingApplication`.`GroupMembers`(groupID, memberID, UsesList) VALUES({groupID}, {custID}, {listNumber});"
                cur.execute(query)
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('groups'))
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


@app.route("/signup/", methods=['GET', 'POST'])
def signUp():

    if request.method == "GET":
        return render_template('signup.html')

    elif request.method == "POST":
        if request.form.get('signUp'):
            cur = mysql.connection.cursor()
            Username = request.form.get('Username')
            Password = request.form.get('Password')
            Password2 = request.form.get('Password2')
            Email = request.form.get('Email')
            StreetName = request.form.get('Street Name')
            UnitNumber = request.form.get('Unit Number')
            phoneNumber = request.form.get('Phone Number')
            userType = request.form.get('userType')

            #CHECK IF USER EXIST
            queryCheck = f"SELECT * FROM User WHERE Email = '{Email}' "
            cur.execute(queryCheck)
            mysql.connection.commit()
            exist = cur.fetchone()
            cur.close()

            # CONDITIONS
            if exist:
                #IF USER EXISTS
                flash("Email already exists", category='error') #ERROR MESSAGE

            elif len(Username) < 1:
                flash("Username required", category='error')

            elif len(Password) < 1:
                flash("Password required", category='error')

            elif Password != Password2:
                flash("Passwords must match", category='error')

            elif len(StreetName) < 1:
                flash("Street name required", category='error')

            elif len(UnitNumber) < 1:
                flash("Unit number required", category='error')

            else:

                #Randomize an ID
                randomID = random.randint(100000000,999999999)
                print(randomID)

                # Go through Users to find a matching ID
                cur = mysql.connection.cursor()
                IDCheck = f"SELECT UserID FROM User WHERE UserID = '{randomID}'"
                cur.execute(IDCheck)
                mysql.connection.commit()
                exist = cur.fetchone()
                cur.close

                #if the ID exist then randomize ID again
                while exist:

                    # Randomize an ID
                    randomID = random.randint(100000000, 999999999)
                    print(randomID)

                    # Go through Users to find a matching ID
                    cur = mysql.connection.cursor()
                    IDCheck = f"SELECT UserID FROM User WHERE UserID = '{randomID}'"
                    cur.execute(IDCheck)
                    mysql.connection.commit()
                    exist = cur.fetchone()
                    cur.close

                    #if it doesnt exist then exit loop

                #set userID to randomID when a unique id is found
                userID = randomID

                #INSERT USER
                cur = mysql.connection.cursor()
                query = f"INSERT INTO `ShoppingApplication`.`User` " \
                        f"(`userID`, `Username`, `Password`, `Email`, `StreetName`, `UnitNumber`) " \
                        f"VALUES ('{userID}', '{Username}', '{Password}', '{Email}', '{StreetName}', '{UnitNumber}')"
                cur.execute(query)
                mysql.connection.commit()
                cur.close()

                cur = mysql.connection.cursor()
                query = f"INSERT INTO `ShoppingApplication`.`UserPhoneNumber` " \
                        f"(`userID`, `PhoneNumber`) " \
                        f"VALUES ('{userID}', '{phoneNumber}')"
                cur.execute(query)
                mysql.connection.commit()
                cur.close()

                if userType == "grocery":
                    #INSERT GROCERYSTORE
                    StoreName = request.form.get('StoreName')
                    cur = mysql.connection.cursor()
                    query = f"INSERT INTO `ShoppingApplication`.`GroceryStore` " \
                            f"(`userID`, `StoreName`) " \
                            f"VALUES ('{userID}', '{StoreName}')"
                    cur.execute(query)
                    mysql.connection.commit()
                    cur.close()
                else:
                    #INSERT CUSTOMER
                    FirstName = request.form.get('FirstName')
                    LastName = request.form.get('LastName')
                    cur = mysql.connection.cursor()
                    query = f"INSERT INTO `ShoppingApplication`.`Customer` " \
                            f"(`userID`, `FirstName`, `LastName`, `CustomerRating`) " \
                            f"VALUES ('{userID}', '{FirstName}', '{LastName}', 5)"
                    cur.execute(query)
                    mysql.connection.commit()
                    cur.close()

                flash("Account created", category='success')

            return redirect(url_for('login'))

        return render_template('signup.html')

    else:
        return render_template('signup.html')


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        Email = request.form.get('Email')
        Password = request.form.get('Password')


        # Find matching username and password
        cur = mysql.connection.cursor()
        query = f"SELECT * FROM User WHERE Email = '{Email}' AND Password = '{Password}'"
        cur.execute(query)
        mysql.connection.commit()
        user=cur.fetchone()
        cur.close()
        print(user)
        #If the user exist and password and username is correct
        if user:

            flash("Log in successful", category='success')
            UID = user[0]
            UName = user[1]
            UPass = user[2]
            UEmail = user[3]
            USTName = user[4]
            UUNumber = user[5]

            print(UID)
            #SAVE USER DATA INTO SESSION
            session['logged_in'] = True
            session['UserID'] = UID
            session['Username'] = UName
            session['Password'] = UPass
            session['Email'] = UEmail
            session['StreetName'] = USTName
            session['UnitNumber'] = UUNumber


            #CHECK IF User is a customer
            cur = mysql.connection.cursor()
            query = f"SELECT * FROM Customer WHERE UserID = {UID}"
            cur.execute(query)
            mysql.connection.commit()
            customer = cur.fetchone()
            cur.close()
            print(customer)
            #If user is already a customer then redirect them to user info page
            if customer:

                #GET Customer data
                cur = mysql.connection.cursor()
                query = f"SELECT * FROM Customer WHERE UserID = '{UID}'"
                cur.execute(query)
                mysql.connection.commit()
                customer = cur.fetchone()
                cur.close()

                session['FName'] = customer[1] #Customers first name
                session['LName'] = customer[2] #Customers second name

                return redirect(url_for('userinfo'))

            #If user is not a customer then direct them to customer sign up page
            else:
                return redirect(url_for('custcreate'))

        else:
            flash("Account not found", category='error')

    return render_template('login.html')


@app.route("/logout/", methods=['GET', 'POST'])
def logout():

    if request.method == "GET":
        return render_template('logout.html')

    elif request.method == "POST":

        session['logged_in'] = False
        session.pop('UserID', None)
        session.pop('Username', None)
        session.pop('Password', None)
        session.pop('Email', None)
        session.pop('StreetName', None)
        session.pop('UnitNumber', None)
        session.pop('FName', None)
        session.pop('LName', None)

        flash("Log out successful!", category='success')

        return redirect(url_for('login'))


    return render_template('logout.html')

@app.route("/custcreate/", methods=['GET', 'POST'])
def custcreate():
    if request.method == 'GET':
        return render_template('custcreate.html')

    elif request.method == "POST":

        FName = request.form.get('FName')
        LName = request.form.get('LName')

        if len(FName) < 1:
            flash("First name required", category='error')
        elif len(LName) < 1:
            flash("Last name required", category='error')
        else:

            flash("Success", category='success')

            UID = session['UserID']

            rating = 5 #default rating

            cur = mysql.connection.cursor()
            query = f"INSERT INTO `ShoppingApplication`.`Customer` " \
                    f"(`UserID`, `FirstName`, `LastName`, `CustomerRating`)" \
                    f"VALUES ('{UID}', '{FName}', '{LName}', '{rating}' )"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()

            session['FName'] = FName
            session['LName'] = LName

            return redirect(url_for('home'))

    return render_template('custcreate.html')


@app.route("/userinfo/", methods=['GET', 'POST'])
def userinfo():
    if request.method == 'GET':

        loggedin = session['logged_in']

        if not loggedin:
            redirect(url_for('login'))

        UID = session['UserID']

        Username = session['Username']
        Password = session['Password']
        Email = session['Email']
        StName = session['StreetName']
        UnitNumber = session['UnitNumber']

        FName = session['FName']
        LName = session['LName']

        #PASS data so html can access data
        return render_template('userinfo.html', UserID = UID, Username = Username, Password = Password, Email = Email, StName = StName, UnitNumber = UnitNumber, FName = FName, LName = LName)

    elif request.method == 'POST':
        return redirect(url_for('edituserinfo'))

    return render_template('userinfo.html')


@app.route("/edituserinfo/", methods=['GET', 'POST'])
def edituserinfo():

    if request.method == 'GET':

        # CHECK IF USER IS LOGGED IN
        loggedin = session['logged_in']

        # REDIRECT TO LOG IN PAGE
        if not loggedin:
            redirect(url_for('login'))

        Username = session['Username']
        Password = session['Password']
        Email = session['Email']
        StName = session['StreetName']
        UnitNumber = session['UnitNumber']

        FName = session['FName']
        LName = session['LName']

        return render_template('edituserinfo.html', Username=Username, Password=Password, Email=Email,
                               StName=StName, UnitNumber=UnitNumber, FName=FName, LName=LName)

    elif request.method == 'POST':

        #USER update data
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        Password2 = request.form.get('Password2')
        Email = request.form.get('Email')
        StreetName = request.form.get('Street Name')
        UnitNumber = request.form.get('Unit Number')


        #CUSTOMER UPDATE data
        Fname = request.form.get('FName')
        Lname = request.form.get('LName')

        # INPUT CONDITIONS
        if len(Fname) < 1:
            flash("First name required", category='error')
        elif len(Lname) < 1:
            flash("Last name required", category='error')
        elif len(Username) < 1:
            flash("Username required", category='error')
        elif len(Password) < 1:
            flash("Password required", category='error')
        elif Password != Password2:
            flash("Password must match", category='error')
        elif len(StreetName) < 1:
            flash("Street name required", category='error')
        elif len(UnitNumber) < 1:
            flash("Unit number required", category='error')
        else:

            #GET USERID
            UID = session['UserID']

            #UPDATE USER QUERY
            cur = mysql.connection.cursor()
            query = f"UPDATE User " \
                    f"SET Username = '{Username}', Password = '{Password}', Email = '{Email}', StreetName = '{StreetName}', UnitNumber = '{UnitNumber}'"\
                    f"WHERE UserID = '{UID}'"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()

            #UPDATE CUSTOMER QUERY
            cur = mysql.connection.cursor()
            query = f"UPDATE Customer " \
                    f"SET FirstName = '{Fname}', LastName = '{Lname}'" \
                    f"WHERE UserID = '{UID}'"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()

            #UPDATE SESSION DATA
            session['Username'] = Username
            session['Password'] = Password
            session['Email'] = Email
            session['StreetName'] = StreetName
            session['UnitNumber'] = UnitNumber

            session['FName'] = Fname
            session['LName'] = Lname

            flash("Edit Successful", category="success")

            return redirect(url_for('userinfo'))


        #DEFAULT VALUES
        Username = session['Username']
        Password = session['Password']
        Email = session['Email']
        StName = session['StreetName']
        UnitNumber = session['UnitNumber']

        FName = session['FName']
        LName = session['LName']

        return render_template('edituserinfo.html', Username=Username, Password=Password, Email=Email,
                               StName=StName, UnitNumber=UnitNumber, FName=FName, LName=LName)

    #DEFAULT VALUES
    Username = session['Username']
    Password = session['Password']
    Email = session['Email']
    StName = session['StreetName']
    UnitNumber = session['UnitNumber']

    FName = session['FName']
    LName = session['LName']

    return render_template('edituserinfo.html',Username=Username, Password=Password, Email=Email,
                               StName=StName, UnitNumber=UnitNumber, FName=FName, LName=LName)

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
    cur = mysql.connection.cursor()
    query = f"SELECT ListNumber From CustomerList WHERE CustomerID = {custID}"
    cur.execute(query)
    mysql.connection.commit()
    results = cur.fetchall()
    results = results[0]
    cur.close()
    if request.method == "POST":
        data = request.form.get('nameID')
        dateInsert = date.today().strftime("%d/%m/%Y")
        insertNumber = max(results) + 1
        if data:
            print(data, "printing...")
            cur = mysql.connection.cursor()
            query = f"INSERT INTO `ShoppingApplication`.`CustomerList`(CustomerID, ListNumber, Name, CreationDate) " \
                    f"VALUES ('{custID}', {insertNumber}, '{data}', {dateInsert});"
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
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
