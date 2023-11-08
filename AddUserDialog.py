# noinspection PyUnresolvedReferences
import time

# noinspection PyUnresolvedReferences
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import *  # Fix for PyCharm hints warnings when using static methods

from CameraHandler import CameraHandler
from DBUtils import DBUtils
from FaceDB import FaceDB
from add_user import Ui_Dialog


class AddUserDialog(QDialog):
    def __init__(self):
        super(AddUserDialog, self).__init__()

        self.filename = None

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.bind_events()

        camera = CameraHandler.get_instance()
        image_name = self.get_image_name()
        camera.capture(image_name)
        self.imageSaved(None, image_name)
        pix_map = QPixmap(image_name)
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.lastImagePreviewLabel.setPixmap(pix_map)
        self.ui.lastImagePreviewLabel.setScaledContents(True)
        self.ui.lastImagePreviewLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.ui.lastImagePreviewLabel.show()

    def bind_events(self):
        self.ui.pushButtonSave.clicked.connect(self.save_user)

    def save_user(self):
        first_name = self.ui.lineEditFirstName.text()
        last_name = self.ui.lineEditLastName.text()
        email = self.ui.lineEditEmail.text()
        mobile = self.ui.lineEditMobile.text()
        username = self.ui.lineEditUsername.text()

        face_db = FaceDB.get_instance()
        face_db.save_user(username, self.filename)

        DBUtils.get_instance().create_user(first_name, last_name, email, mobile, username)

        QMessageBox.about(self, "Face Browser", "User Added")
        self.close()

    def imageSaved(self, id, fileName):
        print(id, fileName)
        self.filename = fileName

    def get_image_name(self):
        millis = int(round(time.time() * 1000))
        return 'faces/{}.png'.format(millis)

    def show(self):
        self.exec_()
