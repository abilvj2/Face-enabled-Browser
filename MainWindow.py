# noinspection PyUnresolvedReferences
# noinspection PyUnresolvedReferences
from functools import reduce

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import *  # Fix for PyCharm hints warnings when using static methods

import Globals
import Utils
from AddDomainDialog import AddDomainDialog
from AddUserDialog import AddUserDialog
from CefWidget import CefWidget
from DBUtils import DBUtils
from NavigationBar import NavigationBar
# Configuration
from RecognizeUserDialog import RecognizeUserDialog

WIDTH = 1080
HEIGHT = 900


class MainWindow(QMainWindow):
    def __init__(self):
        # noinspection PyArgumentList
        super(MainWindow, self).__init__(None)
        # Avoids crash when shutting down CEF (issue #360)
        self.tab_count = 0
        self.cef_widgets = []
        self.current_cef = None

        self.setWindowTitle("Face Browser")

        self.setFocusPolicy(Qt.StrongFocus)
        self.setupLayout()

    def add_user(self):
        user_dialog = AddUserDialog()
        user_dialog.show()

    def add_login_data(self):
        if Globals.current_user:
            domainDialog = AddDomainDialog()
            domainDialog.show()
        else:
            QMessageBox.about(self, "Face Browser", 'No User Logged in')

    def add_menu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        newUser = QAction('New User', self)
        newUser.triggered.connect(self.add_user)

        siteData = QAction('Login Data', self)
        siteData.triggered.connect(self.add_login_data)

        fileMenu.addAction(newUser)
        fileMenu.addAction(siteData)

    def tab_closed(self, index):
        print("close_handler called, index = %s" % index)
        self.tab_count -= 1
        self.tabs.removeTab(index)
        cef_widget = self.cef_widgets[index]
        self.cef_widgets.remove(cef_widget)

        for i in range(len(self.cef_widgets)):
            cef_widget = self.cef_widgets[i]
            cef_widget.index = i
        current_index = self.tabs.currentIndex()
        self.tab_changed(current_index)

    def tab_changed(self, index):
        if self.cef_widgets:
            print('changed tab index', index)
            self.current_cef = self.cef_widgets[index]
            self.navigation_bar.cef_widget = self.current_cef
            self.navigation_bar.updateState()

    def setupLayout(self):
        self.resize(WIDTH, HEIGHT)

        self.add_menu()
        layout = QGridLayout()

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            """QTabWidget::pane {
                border: 0 solid white;
                margin: -12px -12px -12px -12px;
            }"""
        )
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tab_closed)
        self.tabs.currentChanged.connect(self.tab_changed)

        layout.addWidget(self.tabs, 1, 0)
        # layout.addWidget(self.cef_widget, 1, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        # noinspection PyArgumentList
        frame = QFrame()
        frame.setLayout(layout)
        self.setCentralWidget(frame)
        self.navigation_bar = NavigationBar(self.current_cef, self.on_camera_click, self.addNewTab,
                                            self.fill_user_login, self.fill_user_register)
        # noinspection PyArgumentList
        layout.addWidget(self.navigation_bar, 0, 0)

        if Utils.WINDOWS:
            # On Windows with PyQt5 main window must be shown first
            # before CEF browser is embedded, otherwise window is
            # not resized and application hangs during resize.
            self.show()
        self.addNewTab()

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

    def update_tab_title(self, index, text):
        self.tabs.setTabText(index, text)

    def addNewTab(self):

        tab = QWidget()
        cef_widget = CefWidget(self, title_event=self.update_tab_title, index=self.tab_count)
        self.tabs.addTab(tab, "New Tab")

        self.navigation_bar.cef_widget = cef_widget
        cef_widget.embedBrowser("https://www.google.com/")

        tab.layout = QVBoxLayout()
        # tab.layout.addWidget(cef_widget)

        if Utils.LINUX:
            # On Linux with PyQt5 the QX11EmbedContainer widget is
            # no more available. An equivalent in Qt5 is to create
            # a hidden window, embed CEF browser in it and then
            # create a container for that hidden window and replace
            # cef widget in the layout with the container.
            # noinspection PyUnresolvedReferences, PyArgumentList
            container = QWidget.createWindowContainer(cef_widget.hidden_window, parent=tab)
            # noinspection PyArgumentList
            container.setFixedWidth(1280)
            container.setFixedHeight(780)

        tab.layout.addWidget(cef_widget)
        tab.setLayout(tab.layout)
        self.cef_widgets.append(cef_widget)

        self.tabs.setCurrentIndex(self.tab_count)
        self.current_cef = cef_widget

        self.tab_count += 1

    def on_camera_click(self):
        dialog = RecognizeUserDialog(self.on_user_loggedin)
        dialog.show()

    def on_user_loggedin(self):
        self.navigation_bar.enable_user_data()
        message = "{} {} logged in".format(Globals.current_user.first_name, Globals.current_user.last_name)
        self.statusbar.showMessage(message)
        self.current_cef.handle_auto_logout()

    def user_logout(self):
        self.navigation_bar.disable_user_data()
        message = ""
        self.statusbar.showMessage(message)
        QMessageBox.about(self, "Face Browser", "User logged out")

    def fill_user_login(self):
        with open('scripts/fill_login.js', 'r') as event_file:
            lines = event_file.readlines()
            content = str(reduce(lambda x, y: x + ' ' + y, lines))
            self.current_cef.browser.ExecuteJavascript(content)
            url = self.current_cef.browser.GetUrl()
            record = DBUtils.get_instance().get_domain_info(Globals.current_user.user_id, url)
            if record:
                username = record[3]
                password = record[4]
            else:
                username = Globals.current_user.email
                password = ''
            self.current_cef.browser.ExecuteJavascript("fillLogin('{}', '{}')".format(username, password))

    def fill_user_register(self):
        with open('scripts/fill_register.js', 'r') as event_file:
            lines = event_file.readlines()
            content = str(reduce(lambda x, y: x + ' ' + y, lines))
            self.current_cef.browser.ExecuteJavascript(content)
            user = Globals.current_user
            self.current_cef.browser.ExecuteJavascript(
                "fillRegister('{}', '{}', '{}', '{}')".format(
                    user.first_name, user.last_name, user.email, user.mobile)
            )

    def closeEvent(self, event):
        # Close browser (force=True) and free CEF reference
        for cef_widget in self.cef_widgets:
            if cef_widget.browser:
                cef_widget.browser.CloseBrowser(True)
                self.clear_browser_references()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        for cef_widget in self.cef_widgets:
            cef_widget.browser = None
