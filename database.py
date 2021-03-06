import mysql.connector


class Database():
    def __init__(self):
        pass

    @staticmethod
    def createConnection(self):
        config = {
            'user': 'root',  # default user for MySQL
            'password': 'Root_default1996',  # whatever password you set
            'host': 'localhost',
            'database': 'ShoppingApplication',
            'port': '3306',
            'raise_on_warnings': True,

        }
        conn = mysql.connector.connect(**config)
        return conn

    # Triggers.
    def createTriggerCustomerRating1(self):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"CREATE TRIGGER CustomerRating1 " \
                f"AFTER INSERT ON Rates " \
                f"FOR EACH ROW " \
                f"UPDATE Customer " \
                f"SET CustomerRating = ((SELECT COUNT(*) " \
                f"FROM Rates "  \
                f"WHERE rateeID = NEW.rateeID AND Upvote=1)/(SELECT COUNT(*) "  \
				f"FROM Rates "  \
				f"WHERE rateeID=NEW.rateeID)*5) "  \
                f"WHERE UserID=NEW.rateeID"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    # Insertions.
    def insertUser(self, userID, Username, Password, Email, StreetName, UnitNumber):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`User` " \
                f"(`userID`, `Username`, `Password`, `Email`, `StreetName`, `UnitNumber`) " \
                f"VALUES ('{userID}', '{Username}', '{Password}', '{Email}', '{StreetName}', '{UnitNumber}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertUserPhone(self, userID, PhoneNumber):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`UserPhoneNumber` " \
                f"(`userID`, `PhoneNumber`) " \
                f"VALUES ('{userID}', '{PhoneNumber}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertCustomer(self, userID, FirstName, LastName, CustomerRating):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`Customer` " \
                f"(`userID`, `FirstName`, `LastName`, `CustomerRating`) " \
                f"VALUES ('{userID}', '{FirstName}', '{LastName}', '{CustomerRating}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertGrocery(self, userID, StoreName):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`GroceryStore` " \
                f"(`userID`, `StoreName`) " \
                f"VALUES ('{userID}', '{StoreName}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertSale(self, SaleItem, GroceryID, Start, End, Discount):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`SalePromotion` " \
                f"(`SaleItem`, `GroceryId`, `SaleStart`, `SaleEnd`, `Discount`) " \
                f"VALUES ('{SaleItem}', '{GroceryID}', '{Start}', '{End}', '{Discount}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertRating(self, Rater, Ratee, Upvote, DownVote):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`Rates` " \
                f"(`raterID`, `rateeID`, `Upvote`, `Downvote`) " \
                f"VALUES ('{Rater}', '{Ratee}', '{Upvote}', '{DownVote}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

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

    def insertListItem(self, ItemName, ListNumber, CustomerID, Quantity):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`ListItem` " \
                f"(`ItemName`, `ListNumber`, `CustomerID`, `Quantity`) " \
                f"VALUES ('{ItemName}', '{ListNumber}', '{CustomerID}', '{Quantity}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertParty(self, groupID, groupName, creatorID, numberOfMembers, shoppingDate):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`Party` " \
                f"(`groupID`, `groupName`, `creatorID`,  `numberOfMembers`, `shoppingDate`) " \
                f"VALUES ('{groupID}', '{groupName}', '{creatorID}', '{numberOfMembers}', '{shoppingDate}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertGroupMembers(self, groupID, memberID, usesList):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`GroupMembers` " \
                f"(`groupID`, `memberID`, `UsesList`) " \
                f"VALUES ('{groupID}', '{memberID}', '{usesList}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertSaleShownToGroup(self, groupID, saleItem, groceryID):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`SaleShownToGroup` " \
                f"(groupID, saleItem, groceryID) " \
                f"VALUES ('{groupID}', '{saleItem}', '{groceryID}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    def insertReadCustList(self, ListNumber, groupID):
        conn = self.createConnection(self)
        c = conn.cursor()
        query = f"INSERT INTO `ShoppingApplication`.`ReadCustList` " \
                f"(ListNumber, groupID) " \
                f"VALUES ('{ListNumber}', '{groupID}')"
        c.execute(query)
        conn.commit()
        c.close()
        conn.close()

    # This select can probably change. I was just messing around with joining the subclass to the superclass.
    def selectCustomer(self, userID):
        conn = self.createConnection(self)
        c = conn.cursor(buffered=True)
        query = f"SELECT * FROM Customer INNER JOIN User " \
                f"ON Customer.userID = User.userID WHERE Customer.userID = '{userID}'"
        c.execute(query)
        conn.commit()
        results = c.fetchall()
        print(results)
        c.close()
        conn.close()

    def selectUser(self, userID):
        conn = self.createConnection(self)
        c = conn.cursor(buffered=True)
        query = f"SELECT * FROM User WHERE userID = '{userID}'"
        c.execute(query)
        conn.commit()
        results = c.fetchall()
        print(results)
        c.close()
        conn.close()

    def selectAllCustList(self):
        conn = self.createConnection(self)
        c = conn.cursor(buffered=True)
        query = f"SELECT * FROM CustomerList"
        c.execute(query)
        conn.commit()
        results = c.fetchall()
        print(results)
        c.close()
        conn.close()

    def selectAllItems(self, custID, listNumber):
        conn = self.createConnection(self)
        c = conn.cursor(buffered=True)
        query = f"SELECT L.ItemName, L.Quantity " \
                f"FROM ListItem L " \
                f"WHERE customerID = '{custID}' AND listNumber = '{listNumber}'"
        c.execute(query)
        conn.commit()
        results = c.fetchall()
        print(type(results))
        c.close()
        conn.close()
        return results