CREATE SCHEMA superstore_test_db;
-- Drop table Sales;
-- Drop table Orders;
-- Drop table Products;
-- Drop table Category;
-- Drop table Customers;

CREATE TABLE superstore_test_db.customers (
    CustomerID VARCHAR(20) PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Segment VARCHAR(255),
    Country VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(255),
    PostalCode CHAR(5),
    Region VARCHAR(20)
);

CREATE TABLE superstore_test_db.category (
    CategoryID INT PRIMARY KEY, 
    Category VARCHAR(255),
    SubCategory VARCHAR(255)
);

CREATE TABLE superstore_test_db.products (
    ProductID VARCHAR(20) PRIMARY KEY,
    CategoryID INT,
    ProductName VARCHAR(512),
    FOREIGN KEY (CategoryID) REFERENCES category(CategoryID)
);

CREATE TABLE superstore_test_db.orders (
    OrderID VARCHAR(20) PRIMARY KEY,
    OrderDate DATE,
    ShipDate DATE,
    ShipMode VARCHAR(255),
    CustomerID VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID)
);

CREATE TABLE superstore_test_db.sales (
    OrderID VARCHAR(20) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    Sales DECIMAL(10, 2),
    PRIMARY KEY (OrderID, ProductID),
    FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE VIEW superstore_test_db.vw_products AS
Select p.ProductID, p.ProductName, c.Category, c.SubCategory 
From superstore_test_db.products p
LEFT JOIN superstore_test_db.category c ON c.CategoryID = p.CategoryID;

CREATE VIEW superstore_test_db.vw_orders AS
SELECT o.OrderID, o.OrderDate, o.ShipDate, o.ShipMode, o.CustomerID, s.ProductID, s.Sales 
FROM superstore_test_db.orders o RIGHT JOIN superstore_test_db.sales s on o.OrderID = s.OrderID;