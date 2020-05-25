# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cookiewidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CookieWidget(object):
    def setupUi(self, CookieWidget):
        CookieWidget.setObjectName("CookieWidget")
        CookieWidget.resize(300, 71)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CookieWidget.sizePolicy().hasHeightForWidth())
        CookieWidget.setSizePolicy(sizePolicy)
        CookieWidget.setMinimumSize(QtCore.QSize(300, 0))
        CookieWidget.setMaximumSize(QtCore.QSize(310, 16777215))
        self.horizontalLayout = QtWidgets.QHBoxLayout(CookieWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(CookieWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.m_nameLabel = QtWidgets.QLabel(CookieWidget)
        self.m_nameLabel.setObjectName("m_nameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.m_nameLabel)
        self.label_2 = QtWidgets.QLabel(CookieWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.m_domainLabel = QtWidgets.QLabel(CookieWidget)
        self.m_domainLabel.setObjectName("m_domainLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.m_domainLabel)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.m_viewButton = QtWidgets.QPushButton(CookieWidget)
        self.m_viewButton.setObjectName("m_viewButton")
        self.verticalLayout.addWidget(self.m_viewButton)
        self.m_deleteButton = QtWidgets.QPushButton(CookieWidget)
        self.m_deleteButton.setObjectName("m_deleteButton")
        self.verticalLayout.addWidget(self.m_deleteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(CookieWidget)
        QtCore.QMetaObject.connectSlotsByName(CookieWidget)

    def retranslateUi(self, CookieWidget):
        _translate = QtCore.QCoreApplication.translate
        CookieWidget.setWindowTitle(_translate("CookieWidget", "Form"))
        self.label.setText(_translate("CookieWidget", "Name:"))
        self.m_nameLabel.setText(_translate("CookieWidget", "Empty"))
        self.label_2.setText(_translate("CookieWidget", "Domain:"))
        self.m_domainLabel.setText(_translate("CookieWidget", "Emtpy"))
        self.m_viewButton.setText(_translate("CookieWidget", "View"))
        self.m_deleteButton.setText(_translate("CookieWidget", "Delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CookieWidget = QtWidgets.QWidget()
    ui = Ui_CookieWidget()
    ui.setupUi(CookieWidget)
    CookieWidget.show()
    sys.exit(app.exec_())
