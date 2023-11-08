from PyQt5.QtWidgets import QDialog, QMessageBox

import Globals
from DBUtils import DBUtils
from add_domain import UiDomainDialog


class AddDomainDialog(QDialog):
    def __init__(self):
        super(AddDomainDialog, self).__init__()

        self.ui = UiDomainDialog()
        self.ui.setupUi(self)

        self.bind_events()

    def bind_events(self):
        self.ui.pushButtonSave.clicked.connect(self.save_domain)

    def save_domain(self):
        domain = self.ui.lineEditDomain.text()
        username = self.ui.lineEditUsername.text()
        password = self.ui.lineEditPassword.text()

        DBUtils.get_instance().save_domain(Globals.current_user.user_id, domain, username, password)

        QMessageBox.about(self, "Face Browser", "Domain Added")
        self.close()

    def show(self):
        self.exec_()
