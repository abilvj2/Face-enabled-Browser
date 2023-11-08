# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recognize_user.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialogRecognizeUser(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(435, 493)
        self.stackedWidget = QtWidgets.QStackedWidget(Dialog)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 436, 349))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 145, 145))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.stackedWidget.setPalette(palette)
        self.stackedWidget.setObjectName("stackedWidget")
        self.viewfinderPage = QtWidgets.QWidget()
        self.viewfinderPage.setObjectName("viewfinderPage")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.viewfinderPage)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.viewfinder = QCameraViewfinder(self.viewfinderPage)
        self.viewfinder.setObjectName("viewfinder")
        self.gridLayout_5.addWidget(self.viewfinder, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.viewfinderPage)
        self.previewPage = QtWidgets.QWidget()
        self.previewPage.setObjectName("previewPage")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.previewPage)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lastImagePreviewLabel = QtWidgets.QLabel(self.previewPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastImagePreviewLabel.sizePolicy().hasHeightForWidth())
        self.lastImagePreviewLabel.setSizePolicy(sizePolicy)
        self.lastImagePreviewLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.lastImagePreviewLabel.setText("")
        self.lastImagePreviewLabel.setObjectName("lastImagePreviewLabel")
        self.gridLayout_4.addWidget(self.lastImagePreviewLabel, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.previewPage)
        self.pushButtonCapture = QtWidgets.QPushButton(Dialog)
        self.pushButtonCapture.setGeometry(QtCore.QRect(160, 380, 111, 32))
        self.pushButtonCapture.setObjectName("pushButtonCapture")

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(1)
        self.pushButtonCapture.hide()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, dialogRecognizeUser):
        _translate = QtCore.QCoreApplication.translate
        dialogRecognizeUser.setWindowTitle(_translate("dialogRecognizeUser", "Recognize User"))
        self.pushButtonCapture.setText(_translate("dialogRecognizeUser", "Capture"))


from PyQt5.QtMultimediaWidgets import QCameraViewfinder
