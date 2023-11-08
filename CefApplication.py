import os

from cefpython3 import cefpython as cef

# noinspection PyUnresolvedReferences
from PyQt5.QtGui import *
# noinspection PyUnresolvedReferences
from PyQt5.QtCore import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import *  # Fix for PyCharm hints warnings when using static methods


class CefApplication(QApplication):
    def __init__(self, args):
        super(CefApplication, self).__init__(args)
        if not cef.GetAppSetting("external_message_pump"):
            self.timer = self.createTimer()
        self.setupIcon()

    def createTimer(self):
        timer = QTimer()
        # noinspection PyUnresolvedReferences
        timer.timeout.connect(self.onTimer)
        timer.start(10)
        return timer

    def onTimer(self):
        cef.MessageLoopWork()

    def stopTimer(self):
        # Stop the timer after Qt's message loop has ended
        self.timer.stop()

    def setupIcon(self):
        icon_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "resources", "chromium.ico")
        if os.path.exists(icon_file):
            self.setWindowIcon(QIcon(icon_file))
