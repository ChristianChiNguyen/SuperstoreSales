from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from mydbutils import do_query, set_data_to_table_cells, adjust_column_widths
import resources1

class SalesAssociateDialog(QDialog):
    '''
    The Sales Associate dialog
    '''
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('salesassociate.ui')

        # Search Customers
        self._initialize_table_customers()
        self.ui.search_customer_button.clicked.connect(self._load_customers_data)

        # Search Products
        self._initialize_table_products()
        self.ui.search_product_button.clicked.connect(self._load_products_data)

        # Search Orders
        self._initialize_table_orders()
        self.ui.search_order_button.clicked.connect(self._load_orders_data)

    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
        
    def _initialize_table_customers(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.customers_table.clear()

        col = ['  CustomerID  ', '   FirstName  ', '  LastName  ', '  Segment  ', '  Country  ', '  City  ', '  State  ', '  PostalCode  ', '  Region  ']

        self.ui.customers_table.setHorizontalHeaderLabels(col)        
        adjust_column_widths(self.ui.customers_table)

    def _initialize_table_products(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.products_table.clear()

        col = ['  Product ID  ', '   Product Name  ', '  Category  ', '  Sub-Category  ']

        self.ui.products_table.setHorizontalHeaderLabels(col)        
        adjust_column_widths(self.ui.products_table)

    def _initialize_table_orders(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.orders_table.clear()

        col = ['  Order ID  ', '   Order Date  ', '  Ship Date  ', '  Ship Mode  ', '  Customer ID  ', '  Product ID  ', '  Sales  ']

        self.ui.orders_table.setHorizontalHeaderLabels(col)        
        adjust_column_widths(self.ui.orders_table)

    def _load_customers_data(self):
        self._initialize_table_customers()
        customerid = self.ui.customerid.text()
        firstname = self.ui.firstname.text()
        lastname = self.ui.lastname.text()
        segment = self.ui.segment.text()

        sql = """
            SELECT * FROM customers
            WHERE CustomerID like '%""" + customerid + """%'
            AND FirstName like '%""" + firstname + """%'
            AND LastName like '%""" + lastname + """%'
            AND Segment like '%""" + segment + """%'
            ORDER BY FirstName, LastName
            """ 
        
        # print(sql)
        
        # Return data from database
        rows, count = do_query(sql)

        # Set the sales data into the table cells.
        set_data_to_table_cells(self.ui.customers_table, rows, [])
                
        adjust_column_widths(self.ui.customers_table)

    def _load_products_data(self):
        self._initialize_table_products()
        productid = self.ui.productid.text()
        productname = self.ui.productname.text()
        category = self.ui.category.text()
        subcategory = self.ui.subcategory.text()

        sql = """
            SELECT * FROM vw_products
            WHERE ProductID like '%""" + productid + """%'
            AND ProductName like '%""" + productname + """%'
            AND Category like '%""" + category + """%'
            AND SubCategory like '%""" + subcategory + """%'
            ORDER BY ProductID
            """ 
        
        # print(sql)

        # Return data from database
        rows, count = do_query(sql)

        # Set the sales data into the table cells.
        set_data_to_table_cells(self.ui.products_table, rows, [])
                
        adjust_column_widths(self.ui.products_table)

    def _load_orders_data(self):
        self._initialize_table_orders()
        orderid = self.ui.orderid.text()
        shipmod = self.ui.shipmode.text()
        customerid = self.ui.o_customerid.text()
        productid = self.ui.o_productid.text()

        sql = """
            SELECT * FROM vw_orders
            WHERE OrderID like '%""" + orderid + """%'
            AND ShipMode like '%""" + shipmod + """%'
            AND CustomerID like '%""" + customerid + """%'
            AND ProductID like '%""" + productid + """%'
            ORDER BY OrderID
            """ 
        
        # print(sql)
        
        # Return data from database
        rows, count = do_query(sql)

        # Set the sales data into the table cells.
        set_data_to_table_cells(self.ui.orders_table, rows, [])
                
        adjust_column_widths(self.ui.orders_table)