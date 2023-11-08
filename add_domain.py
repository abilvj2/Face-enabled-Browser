# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_domain.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class UiDomainDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(294, 300)
        self.labelDomain = QtWidgets.QLabel(Dialog)
        self.labelDomain.setGeometry(QtCore.QRect(20, 20, 57, 16))
        self.labelDomain.setObjectName("labelDomain")
        self.lineEditDomain = QtWidgets.QLineEdit(Dialog)
        self.lineEditDomain.setGeometry(QtCore.QRect(20, 40, 251, 31))
        self.lineEditDomain.setObjectName("lineEditDomain")
        self.labelUsername = QtWidgets.QLabel(Dialog)
        self.labelUsername.setGeometry(QtCore.QRect(20, 90, 61, 16))
        self.labelUsername.setObjectName("labelUsername")
        self.lineEditUsername = QtWidgets.QLineEdit(Dialog)
        self.lineEditUsername.setGeometry(QtCore.QRect(20, 110, 251, 31))
        self.lineEditUsername.setObjectName("lineEditUsername")
        self.labelPassword = QtWidgets.QLabel(Dialog)
        self.labelPassword.setGeometry(QtCore.QRect(20, 160, 61, 16))
        self.labelPassword.setObjectName("labelPassword")
        self.lineEditPassword = QtWidgets.QLineEdit(Dialog)
        self.lineEditPassword.setGeometry(QtCore.QRect(20, 180, 251, 31))
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.pushButtonSave = QtWidgets.QPushButton(Dialog)
        self.pushButtonSave.setGeometry(QtCore.QRect(90, 240, 121, 32))
        self.pushButtonSave.setObjectName("pushButtonSave")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Domain"))
        self.labelDomain.setText(_translate("Dialog", "Domain"))
        self.labelUsername.setText(_translate("Dialog", "Username"))
        self.labelPassword.setText(_translate("Dialog", "Password"))
        self.pushButtonSave.setText(_translate("Dialog", "Save"))
