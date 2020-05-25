# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 650)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.m_urlLineEdit = QtWidgets.QLineEdit(self.widget)
        self.m_urlLineEdit.setObjectName("m_urlLineEdit")
        self.horizontalLayout.addWidget(self.m_urlLineEdit)
        self.m_urlButton = QtWidgets.QPushButton(self.widget)
        self.m_urlButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.m_urlButton.setIcon(icon)
        self.m_urlButton.setObjectName("m_urlButton")
        self.horizontalLayout.addWidget(self.m_urlButton)
        self.verticalLayout.addWidget(self.widget)
        self.m_webview = QtWebEngineWidgets.QWebEngineView(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m_webview.sizePolicy().hasHeightForWidth())
        self.m_webview.setSizePolicy(sizePolicy)
        self.m_webview.setMinimumSize(QtCore.QSize(0, 0))
        self.m_webview.setObjectName("m_webview")
        self.verticalLayout.addWidget(self.m_webview)
        self.horizontalLayout_2.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralWidget)
        self.frame_2.setMaximumSize(QtCore.QSize(336, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.frame_2)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(87, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.m_newButton = QtWidgets.QPushButton(self.widget_2)
        self.m_newButton.setObjectName("m_newButton")
        self.horizontalLayout_3.addWidget(self.m_newButton)
        self.m_deleteAllButton = QtWidgets.QPushButton(self.widget_2)
        self.m_deleteAllButton.setObjectName("m_deleteAllButton")
        self.horizontalLayout_3.addWidget(self.m_deleteAllButton)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.m_scrollArea = QtWidgets.QScrollArea(self.frame_2)
        self.m_scrollArea.setMinimumSize(QtCore.QSize(320, 0))
        self.m_scrollArea.setMaximumSize(QtCore.QSize(320, 16777215))
        self.m_scrollArea.setWidgetResizable(True)
        self.m_scrollArea.setObjectName("m_scrollArea")
        self.verticalLayout_2.addWidget(self.m_scrollArea)
        self.horizontalLayout_2.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.m_urlLineEdit.returnPressed.connect(self.m_urlButton.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cookie Manager"))
        self.label.setText(_translate("MainWindow", "Cookies:"))
        self.m_newButton.setText(_translate("MainWindow", "New"))
        self.m_deleteAllButton.setText(_translate("MainWindow", "Delete All"))
from PyQt5 import QtWebEngineWidgets
import cookiebrowser_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
