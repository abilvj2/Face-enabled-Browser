# noinspection PyUnresolvedReferences
import os
import time

# noinspection PyUnresolvedReferences
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import *  # Fix for PyCharm hints warnings when using static methods

import Globals
from CameraHandler import CameraHandler
from DBUtils import DBUtils
from FaceRecognitionUtil import FaceRecognitionUtil
from recognize_user import Ui_dialogRecognizeUser


class RecognizeUserDialog(QDialog):
    def __init__(self, recog_callback):
        super(RecognizeUserDialog, self).__init__()

        self.ui = Ui_dialogRecognizeUser()
        self.ui.setupUi(self)

        fileName = self.get_image_name()
        camera = CameraHandler.get_instance()
        camera.capture(fileName)

        face_recognition_util = FaceRecognitionUtil()
        user = face_recognition_util.recognize(fileName)
        if user:
            user = DBUtils.get_instance().get_user(user)
            Globals.current_user = user
            result = 'Found ' + user.first_name
            recog_callback()
        else:
            result = 'No user found'
        QMessageBox.about(self, "Face Browser", result)
        pix_map = QPixmap(fileName)
        self.ui.lastImagePreviewLabel.setPixmap(pix_map)
        self.ui.lastImagePreviewLabel.setScaledContents(True)
        self.ui.lastImagePreviewLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.ui.lastImagePreviewLabel.show()
        os.remove(fileName)

    def get_image_name(self):
        millis = int(round(time.time() * 1000))
        return 'faces/{}.png'.format(millis)

    def show(self):
        self.exec_()
