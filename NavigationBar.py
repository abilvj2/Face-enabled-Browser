import os

# noinspection PyUnresolvedReferences
from PyQt5.QtCore import *
# noinspection PyUnresolvedReferences
from PyQt5.QtGui import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import *  # Fix for PyCharm hints warnings when using static methods


class NavigationBar(QFrame):
    def __init__(self, cef_widget, camera_event, tab_event, login_event, register_event):
        # noinspection PyArgumentList
        super(NavigationBar, self).__init__()
        self.cef_widget = cef_widget

        # Init layout
        layout = QGridLayout()
        self.layout = layout
        self.login_event = login_event
        self.register_event = register_event

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Back button
        self.back = self.createButton("back")
        # noinspection PyUnresolvedReferences
        self.back.clicked.connect(self.onBack)
        # noinspection PyArgumentList
        layout.addWidget(self.back, 0, 0)

        # Forward button
        self.forward = self.createButton("forward")
        # noinspection PyUnresolvedReferences
        self.forward.clicked.connect(self.onForward)
        # noinspection PyArgumentList
        layout.addWidget(self.forward, 0, 1)

        # Reload button
        self.reload = self.createButton("reload")
        # noinspection PyUnresolvedReferences
        self.reload.clicked.connect(self.onReload)
        # noinspection PyArgumentList
        layout.addWidget(self.reload, 0, 2)

        # Url input
        self.url = QLineEdit("")
        self.url.setFixedHeight(30)
        # noinspection PyUnresolvedReferences
        self.url.returnPressed.connect(self.onGoUrl)
        # noinspection PyArgumentList
        layout.addWidget(self.url, 0, 3)

        # Reload button
        self.camera = self.createButton("camera")
        self.camera.clicked.connect(camera_event)
        # noinspection PyArgumentList
        layout.addWidget(self.camera, 0, 4)

        self.add = self.createButton("add")
        self.add.clicked.connect(tab_event)
        # noinspection PyArgumentList
        layout.addWidget(self.add, 0, 5)

        # Layout
        self.setLayout(layout)
        # self.updateState()

    def enable_user_data(self):
        self.login = self.createButton("login")
        self.login.clicked.connect(self.login_event)
        self.layout.addWidget(self.login, 0, 6)

        self.register = self.createButton("register")
        self.register.clicked.connect(self.register_event)
        self.layout.addWidget(self.register, 0, 7)

    def disable_user_data(self):
        self.layout.removeWidget(self.login)
        self.layout.removeWidget(self.register)
        self.login.deleteLater()
        self.login = None
        self.register.deleteLater()
        self.register = None

    def onBack(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.GoBack()

    def onForward(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.GoForward()

    def onReload(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.Reload()

    def onGoUrl(self):
        if self.cef_widget.browser:
            self.cef_widget.browser.LoadUrl(self.url.text())

    def updateState(self):
        browser = self.cef_widget.browser
        if not browser:
            self.back.setEnabled(False)
            self.forward.setEnabled(False)
            self.reload.setEnabled(False)
            self.url.setEnabled(False)
            return
        self.back.setEnabled(browser.CanGoBack())
        self.forward.setEnabled(browser.CanGoForward())
        self.reload.setEnabled(True)
        self.url.setEnabled(True)
        self.url.setText(browser.GetUrl())

    def createButton(self, name):
        resources = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "resources")
        pixmap = QPixmap(os.path.join(resources, "{0}.png".format(name)))
        icon = QIcon(pixmap)
        button = QPushButton()
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())
        return button
