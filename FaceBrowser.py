import ctypes
import os
import platform
import sys

from cefpython3 import cefpython as cef

# noinspection PyUnresolvedReferences
from PyQt5.QtGui import *
# noinspection PyUnresolvedReferences
from PyQt5.QtCore import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import *  # Fix for PyCharm hints warnings when using static methods

import Utils
from CefApplication import CefApplication
from MainWindow import MainWindow


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    settings = {}
    if Utils.MAC:
        # Issue #442 requires enabling message pump on Mac
        # in Qt example. Calling cef.DoMessageLoopWork in a timer
        # doesn't work anymore.
        settings["external_message_pump"] = True

    cef.Initialize(settings)
    app = CefApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.activateWindow()
    main_window.raise_()
    app.exec_()
    if not cef.GetAppSetting("external_message_pump"):
        app.stopTimer()
    del main_window  # Just to be safe, similarly to "del app"
    del app  # Must destroy app object before calling Shutdown
    cef.Shutdown()


def check_versions():
    print("[qt.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[qt.py] Python {ver} {arch}".format(
        ver=platform.python_version(), arch=platform.architecture()[0]))

    print("[qt.py] PyQt {v1} (qt {v2})".format(v1=PYQT_VERSION_STR, v2=qVersion()))
    assert cef.__version__ >= "55.4", "CEF Python v55.4+ required to run this"


if __name__ == '__main__':
    main()
