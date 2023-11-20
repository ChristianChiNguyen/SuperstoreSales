from PyQt5 import uic
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QMessageBox
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


        # # Employees dialog.
        # self._employees_dialog = EmployeesDialog()
        # self.ui.employees_button.clicked.connect(self._show_employees_dialog)
        #
        # # Product Lines dialog.
        # self._productLines_dialog = ProductLinesDialog()
        # self.ui.productLines_button.clicked.connect(self._show_productLines_dialog)