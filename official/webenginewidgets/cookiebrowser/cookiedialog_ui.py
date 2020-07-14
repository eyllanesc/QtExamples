# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cookiedialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from Qt import QtCore, QtGui, QtWidgets


class Ui_CookieDialog(object):
    def setupUi(self, CookieDialog):
        CookieDialog.setObjectName("CookieDialog")
        CookieDialog.resize(400, 245)
        self.formLayout = QtWidgets.QFormLayout(CookieDialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(CookieDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.m_nameLineEdit = QtWidgets.QLineEdit(CookieDialog)
        self.m_nameLineEdit.setReadOnly(True)
        self.m_nameLineEdit.setObjectName("m_nameLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.m_nameLineEdit)
        self.label_2 = QtWidgets.QLabel(CookieDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.m_domainLineEdit = QtWidgets.QLineEdit(CookieDialog)
        self.m_domainLineEdit.setReadOnly(True)
        self.m_domainLineEdit.setObjectName("m_domainLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.m_domainLineEdit)
        self.label_4 = QtWidgets.QLabel(CookieDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.m_pathLineEdit = QtWidgets.QLineEdit(CookieDialog)
        self.m_pathLineEdit.setReadOnly(True)
        self.m_pathLineEdit.setObjectName("m_pathLineEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.m_pathLineEdit)
        self.label_5 = QtWidgets.QLabel(CookieDialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.m_isHttpOnlyComboBox = QtWidgets.QComboBox(CookieDialog)
        self.m_isHttpOnlyComboBox.setObjectName("m_isHttpOnlyComboBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.m_isHttpOnlyComboBox)
        self.label_3 = QtWidgets.QLabel(CookieDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.m_addButton = QtWidgets.QPushButton(CookieDialog)
        self.m_addButton.setEnabled(True)
        self.m_addButton.setObjectName("m_addButton")
        self.horizontalLayout.addWidget(self.m_addButton)
        self.m_cancelButton = QtWidgets.QPushButton(CookieDialog)
        self.m_cancelButton.setObjectName("m_cancelButton")
        self.horizontalLayout.addWidget(self.m_cancelButton)
        self.formLayout.setLayout(8, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.m_isSecureComboBox = QtWidgets.QComboBox(CookieDialog)
        self.m_isSecureComboBox.setObjectName("m_isSecureComboBox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.m_isSecureComboBox)
        self.label_6 = QtWidgets.QLabel(CookieDialog)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.m_valueLineEdit = QtWidgets.QLineEdit(CookieDialog)
        self.m_valueLineEdit.setReadOnly(True)
        self.m_valueLineEdit.setObjectName("m_valueLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.m_valueLineEdit)
        self.m_dateEdit = QtWidgets.QDateEdit(CookieDialog)
        self.m_dateEdit.setReadOnly(True)
        self.m_dateEdit.setObjectName("m_dateEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.m_dateEdit)
        self.label_7 = QtWidgets.QLabel(CookieDialog)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_7)

        self.retranslateUi(CookieDialog)
        self.m_cancelButton.clicked.connect(CookieDialog.reject)
        self.m_addButton.clicked.connect(CookieDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(CookieDialog)
        CookieDialog.setTabOrder(self.m_nameLineEdit, self.m_domainLineEdit)
        CookieDialog.setTabOrder(self.m_domainLineEdit, self.m_valueLineEdit)
        CookieDialog.setTabOrder(self.m_valueLineEdit, self.m_dateEdit)
        CookieDialog.setTabOrder(self.m_dateEdit, self.m_pathLineEdit)
        CookieDialog.setTabOrder(self.m_pathLineEdit, self.m_isHttpOnlyComboBox)
        CookieDialog.setTabOrder(self.m_isHttpOnlyComboBox, self.m_isSecureComboBox)
        CookieDialog.setTabOrder(self.m_isSecureComboBox, self.m_addButton)
        CookieDialog.setTabOrder(self.m_addButton, self.m_cancelButton)

    def retranslateUi(self, CookieDialog):
        _translate = QtCore.QCoreApplication.translate
        CookieDialog.setWindowTitle(_translate("CookieDialog", "Cookie"))
        self.label.setText(_translate("CookieDialog", "Name"))
        self.label_2.setText(_translate("CookieDialog", "Domain"))
        self.label_4.setText(_translate("CookieDialog", "Path"))
        self.label_5.setText(_translate("CookieDialog", "isHttpOnly"))
        self.label_3.setText(_translate("CookieDialog", "isSecure"))
        self.m_addButton.setText(_translate("CookieDialog", "Add"))
        self.m_cancelButton.setText(_translate("CookieDialog", "Cancel"))
        self.label_6.setText(_translate("CookieDialog", "Value"))
        self.label_7.setText(_translate("CookieDialog", "Expires"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CookieDialog = QtWidgets.QDialog()
    ui = Ui_CookieDialog()
    ui.setupUi(CookieDialog)
    CookieDialog.show()
    sys.exit(app.exec_())
