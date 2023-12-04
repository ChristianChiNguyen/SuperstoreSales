from mysql.connector import Error
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from mydbutils import do_query, insert_query
import resources1

class DBAdminDialog(QDialog):
    '''
    The quering data dialog
    '''

    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('dbadmin.ui')

        # Create Customer
        self.ui.create_customer_button.clicked.connect(self._insert_customer_data)

        # Create Product
        self._initialize_category_menu()
        self._initialize_sub_category_menu()
        self.ui.category_cb.currentIndexChanged.connect(self._initialize_sub_category_menu)
        self.ui.create_product_button.clicked.connect(self._insert_product_data)

    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

    def _insert_customer_data(self):
        """
        Insert Customer data from the UI
        """

        customerid = self.ui.customerid.text()
        firstname = self.ui.firstname.text()
        lastname = self.ui.lastname.text()
        segment = self.ui.segment.text()
        country = self.ui.country.text()
        city = self.ui.city.text()
        state = self.ui.state.text()
        postalcode = self.ui.postalcode.text()
        region = self.ui.region.text()

        if customerid == '' or firstname == '' or lastname == '' or segment == '' or country == '' or city == '' or state == '' or postalcode == '' or region == '':
            self.ui.customer_check.setText(" Please fill all the fields !")
            return
        
        # Check if CustomerID already exists

        sql = """
            SELECT * FROM customers
            WHERE CustomerID = '""" + customerid + """'
            """
        
        # Return data from database
        rows, count = do_query(sql)

        if rows:
            self.ui.customer_check.setText(" Customer ID already exists !")
            return
        
        values = (customerid,firstname,lastname,segment,country,city,state,postalcode,region)

        try:
            insert_query("customers", values)
            self.ui.customer_check.setText(" Customer has been created ! ")
        except Error as e:
            self.ui.customer_check.setText(" Query failed, invalid data !")

    def _initialize_category_menu(self):
        """
        Initialize the category menu of products
        """
        sql = """
            SELECT distinct Category FROM category
            ORDER BY category
            """
        rows_category, _ = do_query(sql)

        # Set the menu items to the category
        for row in rows_category:
            c = row[0]
            self.ui.category_cb.addItem(c, row)

    def _initialize_sub_category_menu(self):
        """
        Initialize the city menu of clients' location from the database.
        """
        self.ui.subcategory_cb.clear()
        category = self.ui.category_cb.currentData()
        _category = category[0]
        sql = """
            SELECT distinct SubCategory FROM category
            WHERE Category = '""" + _category + """' ORDER BY SubCategory
            """ 
        
        rows_subcategory, _ = do_query(sql)

        # Set the menu items to the city by selected country
        for row in rows_subcategory:
            c = row[0]
            self.ui.subcategory_cb.addItem(c, row)

    def _insert_product_data(self):
        """
        Insert Product data from the UI
        """

        productid = self.ui.productid.text()
        productname = self.ui.productname.toPlainText()
        _category = self.ui.category_cb.currentData()
        category = _category[0]
        _subcategory = self.ui.subcategory_cb.currentData()
        subcategory = _subcategory[0]

        if productid == '' or productname == '':
            self.ui.product_check.setText(" Please fill all the fields !")
            return
        
        # Check if ProductID already exists

        sql = """
            SELECT * FROM products
            WHERE ProductID = '""" + productid + """'
            """
        
        # Return data from database
        rows, count = do_query(sql)

        if rows:
            self.ui.product_check.setText(" Product ID already exists !")
            return
        
        # Get the Category ID

        sql = """
            SELECT CategoryID FROM category
            WHERE Category = '""" + category + """'
            AND SubCategory = '""" + subcategory + """'
            """
        
        # Return data from database
        rows, count = do_query(sql)

        for row in rows:
            categoryid = row[0]
        
        values = (productid, categoryid, productname)

        try:
            insert_query("products", values)
            self.ui.product_check.setText(" Product has been created ! ")
        except Error as e:
            self.ui.product_check.setText(" Query failed, invalid data !")
