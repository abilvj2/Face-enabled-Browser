import ctypes
import sys
# noinspection PyUnresolvedReferences
import threading
# noinspection PyUnresolvedReferences
import time

from PyQt5.QtGui import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import *  # Fix for PyCharm hints warnings when using static methods
from cefpython3 import cefpython as cef

import Utils

WindowUtils = cef.WindowUtils()
CefWidgetParent = QWidget

INACTIVE_INTERVAL = 10


class CefWidget(CefWidgetParent):
    def __init__(self, parent=None, title_event=None, index=0):
        # noinspection PyArgumentList
        super(CefWidget, self).__init__(parent)
        self.parent = parent
        self.browser = None
        self.hidden_window = None  # Required for PyQt5 on Linux
        self.show()
        self.tab_event = title_event
        self.index = index
        self.setMouseTracking(True)
        self.last_active_time = time.time()

    def handle_auto_logout(self):
        self.last_active_time = time.time()
        timer = threading.Timer(INACTIVE_INTERVAL, self.check_inactive_time)
        timer.start()

    def check_inactive_time(self):
        time_diff = time.time() - self.last_active_time
        if time_diff > INACTIVE_INTERVAL:
            self.parent.user_logout()
        else:
            self.handle_auto_logout()

    def mouseMoveEvent(self, e):
        self.last_active_time = time.time()

    def focusInEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if self.browser:
            if Utils.WINDOWS:
                WindowUtils.OnSetFocus(self.getHandle(), 0, 0, 0)
            self.browser.SetFocus(True)

    def focusOutEvent(self, event):
        # This event seems to never get called on Linux, as CEF is
        # stealing all focus due to Issue #284.
        if self.browser:
            self.browser.SetFocus(False)

    def embedBrowser(self, url):
        if Utils.LINUX:
            # noinspection PyUnresolvedReferences
            self.hidden_window = QWindow()
            self.hidden_window.setHeight(700)
            self.hidden_window.setWidth(700)
        window_info = cef.WindowInfo()
        rect = [0, 0, self.width(), self.height()]
        window_info.SetAsChild(self.getHandle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url=url)
        self.browser.SetClientHandler(LoadHandler(self.parent.navigation_bar))
        self.browser.SetClientHandler(FocusHandler(self))
        self.browser.SetClientHandler(ContentHandler(self))

    def title_event(self, text):
        self.tab_event(self.index, text)

    def getHandle(self):
        if self.hidden_window:
            # PyQt5 on Linux
            return int(self.hidden_window.winId())
        try:
            # PyQt4 and PyQt5
            return int(self.winId())
        except:
            # PySide:
            # | QWidget.winId() returns <PyCObject object at 0x02FD8788>
            # | Converting it to int using ctypes.
            if sys.version_info[0] == 2:
                # Python 2
                ctypes.pythonapi.PyCObject_AsVoidPtr.restype = (
                    ctypes.c_void_p)
                ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = (
                    [ctypes.py_object])
                return ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
            else:
                # Python 3
                ctypes.pythonapi.PyCapsule_GetPointer.restype = (
                    ctypes.c_void_p)
                ctypes.pythonapi.PyCapsule_GetPointer.argtypes = (
                    [ctypes.py_object])
                return ctypes.pythonapi.PyCapsule_GetPointer(
                    self.winId(), None)

    def moveEvent(self, _):
        self.x = 0
        self.y = 0
        if self.browser:
            if Utils.WINDOWS:
                WindowUtils.OnSize(self.getHandle(), 0, 0, 0)
            elif Utils.LINUX:
                self.browser.SetBounds(self.x, self.y,
                                       self.width(), self.height())
            self.browser.NotifyMoveOrResizeStarted()

    def resizeEvent(self, event):
        size = event.size()
        if self.browser:
            if Utils.WINDOWS:
                WindowUtils.OnSize(self.getHandle(), 0, 0, 0)
            elif Utils.LINUX:
                self.browser.SetBounds(self.x, self.y,
                                       size.width(), size.height())
            self.browser.NotifyMoveOrResizeStarted()


class LoadHandler(object):
    def __init__(self, navigation_bar):
        self.initial_app_loading = True
        self.navigation_bar = navigation_bar

    def OnLoadingStateChange(self, **_):
        self.navigation_bar.updateState()

    def OnLoadStart(self, browser, **_):
        self.navigation_bar.url.setText(browser.GetUrl())
        if self.initial_app_loading:
            self.navigation_bar.cef_widget.setFocus()
            # Temporary fix no. 2 for focus issue on Linux (Issue #284)
            if Utils.LINUX:
                print("[qt.py] LoadHandler.OnLoadStart:"
                      " keyboard focus fix no. 2 (Issue #284)")
                browser.SetFocus(True)
            self.initial_app_loading = False


class FocusHandler(object):
    def __init__(self, cef_widget):
        self.cef_widget = cef_widget

    def OnSetFocus(self, **_):
        pass

    def OnGotFocus(self, browser, **_):
        # Temporary fix no. 1 for focus issues on Linux (Issue #284)
        if Utils.LINUX:
            print("[qt.py] FocusHandler.OnGotFocus:"
                  " keyboard focus fix no. 1 (Issue #284)")
            browser.SetFocus(True)


class ContentHandler:
    def __init__(self, cef_widget):
        self.widget = cef_widget

    def OnTitleChange(self, browser, title):
        print(title)
        title = title[:10] + (title[10:] and '..')
        self.widget.title_event(title)
