from PyQt5 import uic
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QMessageBox
import resources
from Querying import QueryingDialog
import resources1

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


        # Querying dialog.
        self._quering_dialog = QueryingDialog()
        self.ui.querying_sales_button.clicked.connect(self._show_querying_dialog)
        #
        # # Product Lines dialog.
        # self._productLines_dialog = ProductLinesDialog()
        # self.ui.productLines_button.clicked.connect(self._show_productLines_dialog)

    def _show_querying_dialog(self):
        """
        Show the querying dialog.
        """
        self._quering_dialog.show_dialog()