CREATE DATABASE ShoppingApplication;

CREATE TABLE `ShoppingApplication`.`User`(
`UserID` INT NOT NULL CHECK (`UserID` BETWEEN 100000000 AND 999999999),
`Username` VARCHAR(45),
`Password` VARCHAR(45),
`Email` VARCHAR(45),
`StreetName` VARCHAR(45),
`UnitNumber` INT,
PRIMARY KEY(`UserID`));

CREATE TABLE `ShoppingApplication`.`UserPhoneNumber`(
`UserID` INT NOT NULL,
`PhoneNumber` VARCHAR(22) NOT NULL,
FOREIGN KEY (`UserID`) REFERENCES User(`UserID`),
PRIMARY KEY(`PhoneNumber`, `UserID`));

CREATE TABLE `ShoppingApplication`.`GroceryStore`(
`UserID` INT NOT NULL,
`StoreName` VARCHAR(45),
FOREIGN KEY (`UserID`) REFERENCES User(`UserID`),
PRIMARY KEY (`UserID`));

CREATE TABLE `ShoppingApplication`.`Customer`(
`UserID` INT NOT NULL,
`FirstName` VARCHAR(45),
`LastName` VARCHAR(45),
`CustomerRating` INT,
FOREIGN KEY (`UserID`) REFERENCES User(`UserID`),
PRIMARY KEY (`UserID`));

CREATE TABLE `ShoppingApplication`.`SalePromotion`(
`SaleItem` VARCHAR(45) NOT NULL,
`GroceryID` INT NOT NULL,
`SaleStart` DATE,
`SaleEnd` DATE,
`Discount` FLOAT,
CHECK (`SaleStart` < `SaleEnd`),
FOREIGN KEY (`GroceryID`) REFERENCES GroceryStore(`UserID`),
PRIMARY KEY (`SaleItem`, `GroceryID`));

CREATE TABLE `ShoppingApplication`.`Rates`(
`raterID` INT NOT NULL,
`rateeID` INT NOT NULL,
`Upvote` INT NULL,
`Downvote` INT NULL,
CHECK (`raterID` <> `rateeID`),
ChECK (`UpVote` <> `Downvote`),
FOREIGN KEY (`raterID`) REFERENCES Customer(`UserID`),
FOREIGN KEY (`rateeID`) REFERENCES Customer(`UserID`),
PRIMARY KEY (`raterID`, `rateeID`));

CREATE TABLE `ShoppingApplication`.`CustomerList`(
`CustomerID` INT NOT NULL,
`ListNumber` INT NOT NULL,
`Name` VARCHAR(45),
`CreationDate` DATE,
FOREIGN KEY (`CustomerID`) REFERENCES Customer(`UserID`),
PRIMARY KEY (`ListNumber`, `CustomerID`));

CREATE TABLE `ShoppingApplication`.`ListItem`(
`ItemName` VARCHAR(45) NOT NULL,
`ListNumber` INT NOT NULL,
`CustomerID` INT NOT NULL,
`Quantity` INT,
CONSTRAINT FOREIGN KEY (`ListNumber`, `CustomerID`) REFERENCES CustomerList(`ListNumber`, `CustomerID`) ON DELETE CASCADE,
PRIMARY KEY (`ItemName`, `ListNumber`, `CustomerID`));

CREATE TABLE `ShoppingApplication`.`Party`(
`groupID` INT NOT NULL CHECK (`groupID` BETWEEN 1000000 AND 9999999),
`creatorID` INT NOT NULL CHECK (`creatorID` BETWEEN 100000000 AND 999999999),
`groupName` VARCHAR(45),
`numberOfMembers` INT,
`shoppingDate` DATE,
FOREIGN KEY (`creatorID`) REFERENCES Customer(`UserID`),
PRIMARY KEY (`groupID`)
);

CREATE TABLE `ShoppingApplication`.`GroupMembers`(
`groupID` INT NOT NULL,
`memberID` INT NOT NULL,
`UsesList` INT NOT NULL,
CONSTRAINT FOREIGN KEY (`groupID`) REFERENCES Party (`groupID`) ON DELETE CASCADE,
FOREIGN KEY (`memberID`) REFERENCES Customer(`UserID`),
FOREIGN KEY (`UsesList`, `memberID`) REFERENCES CustomerList(`ListNumber`, `CustomerID`),
PRIMARY KEY (`groupID`, `memberID`)
);

CREATE TABLE `ShoppingApplication`.`SaleShownToGroup`(
`groupID` INT NOT NULL,
`saleItem` VARCHAR(45) NOT NULL,
`groceryID` INT NOT NULL,
FOREIGN KEY (`groupID`) REFERENCES Party (`groupID`),
FOREIGN KEY (`saleItem`, `groceryID`) REFERENCES SalePromotion (`saleItem`, `groceryID`),
PRIMARY KEY (`groupID`, `saleItem`, `groceryID`)
);


