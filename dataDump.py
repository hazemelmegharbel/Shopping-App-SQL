import mysql.connector
from database import Database

db = Database()

#insertUser(userID, Username, Password, Email, StreetName, UnitNumber)
db.insertUser('100111111', 'Walmart_1', 'wally_wally_world', 'walmart@gmail.com', 'Highway 1', '145')
db.insertUser('101111111', 'Walmart_2', 'wally_wally_world2', 'walmart2@gmail.com', 'Renfrew', '3333')
db.insertUser('111111111', 'Walmart_3', 'wally_wally_world3', 'walmart3@gmail.com', 'Hastings Street', '4556')
db.insertUser('100000011', 'StoreUsername123', 'securePassword', 'ProfessionalEmail@gmail.com', 'Granville street', '309')
db.insertUser('100001111', 'StoreUsername1234', 'secureP@ssW0rd', 'Store@gmail.com', 'Knight Street', '888')
db.insertUser('100000001', 'Username123', 'password123', 'fakeEmail@gmail.com', 'main street', '1159')
db.insertUser('100000111', 'Mamajama1337', 'snugglesIsMyDog', 'snuggles@hotmail.com', 'Broadway street', '2222')
db.insertUser('100011111', 'CoolGrandma', 'CookiesForMyGrandkids', 'Grandma@gmail.com', 'Main street', '6697')
db.insertUser('222222222', 'I_LoveGroceries', '123', 'GroceryShopper@Telus.ca', 'Hastings street', '335')
db.insertUser('444444444', 'SlowJams1972', 'password_123', 'email@gmail.com', 'Marine Drive', '777')
db.insertUser('555555555', 'IceTeaDrinker', 'BriskLover', 'icedTea@hotmail.com', 'Oak Street', '888')
db.insertUser('666666666', 'FamJamCam', 'Jamming2Hard4U', 'Cameron_Samson@gmail.com', 'Arbutus', '666')
db.insertUser('777777777', 'SammiesAccount', '@ppl3sAnd0ranges', 'Samantha_Smith@gmail.com', 'Oak Street', '9012')

#insertUserPhone(userID, PhoneNumber)
db.insertUserPhone('100001111', '7781234567')
db.insertUserPhone('100001111', '6045565657')
db.insertUserPhone('100000001', '7881003435')
db.insertUserPhone('444444444', '6043333678')
db.insertUserPhone('777777777', '7781230990')

#insertGrocery(userID, StoreName)
db.insertGrocery('100111111', 'Walmart')
db.insertGrocery('101111111', 'Walmart')
db.insertGrocery('111111111', 'Walmart')
db.insertGrocery('100000011', 'Mikes Store')
db.insertGrocery('100001111', 'Donalds Market')

#insertCustomer(userID, FirstName, LastName, CustomerRating)
db.insertCustomer('100000001', 'Evan', 'Mulliamy')
db.insertCustomer('100000111', 'Teresa', 'McLaughland')
db.insertCustomer('100011111', 'Candice', 'Lovelace')
db.insertCustomer('222222222', 'Jimmy', 'Wu')
db.insertCustomer('444444444', 'Charlie', 'Smith')
db.insertCustomer('555555555', 'Sophie', 'Wood')
db.insertCustomer('666666666', 'Cameron', 'Samson')
db.insertCustomer('777777777', 'Samantha', 'Smith')

#insertSale(SaleItem, GroceryID, Start, End, Discount)
db.insertSale('Bananas', '100111111', '2021-09-02', '2021-10-30', '0.1')
db.insertSale('Hand Sanitizer', '100111111', '2022-01-01', '2022-02-28', '0.7')
db.insertSale('Instant Noodles', '100001111', '2021-07-30', '2021-08-30', '0.2')
db.insertSale('Toilet Paper', '100000011', '2022-01-01', '2022-03-30', '0.3')
db.insertSale('Apples', '111111111', '2021-08-03', '2021-09-03', '0.1')

#insertParty(groupID, groupName, creatorID, shoppingDate)
db.insertParty('1000001', 'BestShoppers', '100011111', '2021-10-03')
db.insertParty('1000002', 'ShopTeamNumber1', '222222222', '2021-10-03')
db.insertParty('1000022', 'L337Shoppers', '666666666', '2021-11-03')
db.insertParty('1000032', 'ShopsSoFast', '666666666', '2021-12-03')
db.insertParty('1000044', 'AppleFans333', '555555555', '2021-11-03')

#insertGroupMembers(groupID, memberID)
db.insertGroupMembers('1000001', '100011111')
db.insertGroupMembers('1000002', '222222222')
db.insertGroupMembers('1000022', '666666666')
db.insertGroupMembers('1000032', '666666666')
db.insertGroupMembers('1000032', '100000111')
db.insertGroupMembers('1000032', '777777777')
db.insertGroupMembers('1000044', '555555555')

#insertRating(Rater, Ratee, Upvote, DownVote)
db.insertRating('666666666', '777777777', 1, 0)
db.insertRating('777777777', '666666666', 1, 0)
db.insertRating('777777777', '100000111', 0, 1)
db.insertRating('100000111', '777777777', 0, 1)
db.insertRating('666666666', '100000111', 1, 0)

#insertCustomerList(ListNumber, CreationDate, CustomerID)
db.insertCustomerList('1', 'myList1', '2021-01-21', '100000001')
db.insertCustomerList('1', 'shoppingList', '2021-02-28', '100000111')
db.insertCustomerList('1', 'To buy on sunday', '2021-03-01', '222222222')
db.insertCustomerList('4', 'partyPrep', '2021-02-02', '666666666')
db.insertCustomerList('5', 'shoppingList2',  '2021-02-20', '100000111')

#insertListItem(ItemName, ListNumber, CustomerID, Quantity)
db.insertListItem('Strawberries', '1', '100000001', '3')
db.insertListItem('French bread', '1', '100000001', '2')
db.insertListItem('Bananas', '1', '100000001', '2')
db.insertListItem('Oranges', '1', '100000001', '4')
db.insertListItem('Toilet Paper', '1', '100000111', '2')
db.insertListItem('Hot Dogs', '1', '222222222', '2')
db.insertListItem('Oreos', '4', '666666666', '5')
db.insertListItem('BBQ Chips', '5', '100000111', '3')
#can't get 200g of NUTS lmao

#insertSaleShownToGroup(groupID, saleItem, groceryID)
db.insertSaleShownToGroup('1000001', 'Bananas', '100111111')
db.insertSaleShownToGroup('1000002', 'Hand Sanitizer', '100111111')
db.insertSaleShownToGroup('1000022', 'Instant Noodles', '100001111')
db.insertSaleShownToGroup('1000032', 'Instant Noodles', '100001111')
db.insertSaleShownToGroup('1000032', 'Toilet Paper', '100000011')
db.insertSaleShownToGroup('1000044', 'Apples', '111111111')

print('Sent to DB!\n')