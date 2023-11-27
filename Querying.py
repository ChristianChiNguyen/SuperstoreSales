import sys
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QGraphicsScene, QGraphicsView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mydbutils import do_query, set_data_to_table_cells, adjust_column_widths
import resources1

class QueryingDialog(QDialog):
    '''
    The quering data dialog
    '''

    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('querying.ui')

        # Search Customers
        self._initialize_table_customers()
        self.ui.search_customer_button.clicked.connect(self._load_customers_data)

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
        
        print(sql)
        
        # Return data from database
        rows, count = do_query(sql)

        # Set the sales data into the table cells.
        set_data_to_table_cells(self.ui.customers_table, rows, [])
                
        adjust_column_widths(self.ui.customers_table)
