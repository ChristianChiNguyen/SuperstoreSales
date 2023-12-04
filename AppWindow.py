from PyQt5 import uic
from PyQt5.QtGui import QWindow
from SalesAssociate import SalesAssociateDialog
from Customer import CustomerDialog
from DBAdmin import DBAdminDialog
import resources

class AppWindow(QWindow):
    """
    The main application window.
    """

    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()

        self.ui = uic.loadUi('app_main.ui')
        self.ui.show()


        # Sales Associate dialog.
        self._sales_associate_dialog = SalesAssociateDialog()
        self.ui.sales_associate_button.clicked.connect(self._show_sales_associate_dialog)

        # Customer dialog.
        self._customer_dialog = CustomerDialog()
        self.ui.customer_button.clicked.connect(self._show_customer_dialog)
        
        # DB Admin dialog.
        self._db_admin_dialog = DBAdminDialog()
        self.ui.db_admin_button.clicked.connect(self._show_db_admin_dialog)

    def _show_sales_associate_dialog(self):
        """
        Show the Sales Associate dialog.
        """
        self._sales_associate_dialog.show_dialog()
        
    def _show_customer_dialog(self):
        """
        Show the Customer dialog.
        """
        self._customer_dialog.show_dialog()
    
    def _show_db_admin_dialog(self):
        """
        Show the DB Admin dialog.
        """
        self._db_admin_dialog.show_dialog()