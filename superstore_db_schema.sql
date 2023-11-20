-- Drop table Sales;
-- Drop table Orders;
-- Drop table Products;
-- Drop table Category;
-- Drop table Customers;

CREATE TABLE Customers (
    CustomerID VARCHAR(20) PRIMARY KEY,
    CustomerName VARCHAR(255),
    Segment VARCHAR(255),
    Country VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(255),
    PostalCode CHAR(5),
    Region VARCHAR(20)
);
CREATE TABLE Category (
    CategoryID INT PRIMARY KEY, 
    Category VARCHAR(255),
    SubCategory VARCHAR(255)
);
CREATE TABLE Products (
    ProductID VARCHAR(20) PRIMARY KEY,
    CategoryID INT,
    ProductName VARCHAR(512),
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
);
CREATE TABLE Orders (
    OrderID VARCHAR(20) PRIMARY KEY,
    OrderDate DATE,
    ShipDate DATE,
    ShipMode VARCHAR(255),
    CustomerID VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
CREATE TABLE Sales (
    OrderID VARCHAR(20) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    Sales DECIMAL(10, 2),
    PRIMARY KEY (OrderID, ProductID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
