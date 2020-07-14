# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stylewidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from Qt.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                       QObject, QPoint, QRect, QSize, Qt, QTime, QUrl)
from Qt.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                      QFontDatabase, QIcon, QKeySequence, QLinearGradient,
                      QPainter, QPalette, QPixmap, QRadialGradient)
from Qt.QtWidgets import *

import styleexample_rc


class Ui_StyleWidget(object):
    def setupUi(self, StyleWidget):
        if not StyleWidget.objectName():
            StyleWidget.setObjectName(u"StyleWidget")
        StyleWidget.resize(184, 245)
        self.gridLayout = QGridLayout(StyleWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(StyleWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.transparentStyle = QPushButton(self.groupBox)
        self.transparentStyle.setObjectName(u"transparentStyle")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transparentStyle.sizePolicy().hasHeightForWidth())
        self.transparentStyle.setSizePolicy(sizePolicy)
        self.transparentStyle.setFocusPolicy(Qt.StrongFocus)
        self.transparentStyle.setCheckable(True)
        self.transparentStyle.setChecked(False)
        self.transparentStyle.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.transparentStyle, 0, 0, 1, 1)

        self.blueStyle = QPushButton(self.groupBox)
        self.blueStyle.setObjectName(u"blueStyle")
        sizePolicy.setHeightForWidth(self.blueStyle.sizePolicy().hasHeightForWidth())
        self.blueStyle.setSizePolicy(sizePolicy)
        self.blueStyle.setFocusPolicy(Qt.StrongFocus)
        self.blueStyle.setCheckable(True)
        self.blueStyle.setChecked(False)
        self.blueStyle.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.blueStyle, 2, 0, 1, 1)

        self.khakiStyle = QPushButton(self.groupBox)
        self.khakiStyle.setObjectName(u"khakiStyle")
        sizePolicy.setHeightForWidth(self.khakiStyle.sizePolicy().hasHeightForWidth())
        self.khakiStyle.setSizePolicy(sizePolicy)
        self.khakiStyle.setFocusPolicy(Qt.StrongFocus)
        self.khakiStyle.setCheckable(True)
        self.khakiStyle.setChecked(False)
        self.khakiStyle.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.khakiStyle, 0, 1, 1, 1)

        self.noStyle = QPushButton(self.groupBox)
        self.noStyle.setObjectName(u"noStyle")
        sizePolicy.setHeightForWidth(self.noStyle.sizePolicy().hasHeightForWidth())
        self.noStyle.setSizePolicy(sizePolicy)
        self.noStyle.setFocusPolicy(Qt.StrongFocus)
        self.noStyle.setCheckable(True)
        self.noStyle.setChecked(True)
        self.noStyle.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.noStyle, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 1, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(StyleWidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(StyleWidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setFocusPolicy(Qt.WheelFocus)
        self.spinBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.spinBox.setKeyboardTracking(False)

        self.horizontalLayout.addWidget(self.spinBox)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)

        self.horizontalScrollBar = QScrollBar(StyleWidget)
        self.horizontalScrollBar.setObjectName(u"horizontalScrollBar")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.horizontalScrollBar.sizePolicy().hasHeightForWidth())
        self.horizontalScrollBar.setSizePolicy(sizePolicy2)
        self.horizontalScrollBar.setMinimumSize(QSize(0, 24))
        self.horizontalScrollBar.setFocusPolicy(Qt.TabFocus)
        self.horizontalScrollBar.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalScrollBar, 3, 0, 1, 1)

        self.horizontalScrollBar_2 = QScrollBar(StyleWidget)
        self.horizontalScrollBar_2.setObjectName(u"horizontalScrollBar_2")
        sizePolicy2.setHeightForWidth(self.horizontalScrollBar_2.sizePolicy().hasHeightForWidth())
        self.horizontalScrollBar_2.setSizePolicy(sizePolicy2)
        self.horizontalScrollBar_2.setMinimumSize(QSize(0, 24))
        self.horizontalScrollBar_2.setFocusPolicy(Qt.TabFocus)
        self.horizontalScrollBar_2.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalScrollBar_2, 3, 1, 1, 1)

        self.pushButton_2 = QPushButton(StyleWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy2.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy2)
        self.pushButton_2.setFocusPolicy(Qt.StrongFocus)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setChecked(True)
        self.pushButton_2.setFlat(False)

        self.gridLayout.addWidget(self.pushButton_2, 4, 0, 1, 1)

        self.pushButton = QPushButton(StyleWidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)
        self.pushButton.setFocusPolicy(Qt.StrongFocus)
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(True)
        self.pushButton.setFlat(False)

        self.gridLayout.addWidget(self.pushButton, 4, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 0, 1, 2)

        self.spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.spacerItem, 6, 0, 1, 1)

        self.close = QPushButton(StyleWidget)
        self.close.setObjectName(u"close")
        self.close.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout.addWidget(self.close, 6, 1, 1, 1)


        self.retranslateUi(StyleWidget)
        self.horizontalScrollBar.valueChanged.connect(self.horizontalScrollBar_2.setValue)
        self.horizontalScrollBar_2.valueChanged.connect(self.horizontalScrollBar.setValue)
        self.pushButton.clicked.connect(self.horizontalScrollBar_2.setEnabled)
        self.pushButton_2.clicked.connect(self.horizontalScrollBar.setVisible)
        self.spinBox.valueChanged.connect(self.horizontalScrollBar_2.setValue)
        self.horizontalScrollBar_2.valueChanged.connect(self.spinBox.setValue)

        QMetaObject.connectSlotsByName(StyleWidget)
    # setupUi

    def retranslateUi(self, StyleWidget):
        StyleWidget.setWindowTitle(QCoreApplication.translate("StyleWidget", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("StyleWidget", u"Styles", None))
        self.transparentStyle.setText(QCoreApplication.translate("StyleWidget", u"Transp.", None))
        self.blueStyle.setText(QCoreApplication.translate("StyleWidget", u"Blue", None))
        self.khakiStyle.setText(QCoreApplication.translate("StyleWidget", u"Khaki", None))
        self.noStyle.setText(QCoreApplication.translate("StyleWidget", u"None", None))
        self.label.setText(QCoreApplication.translate("StyleWidget", u"Value:", None))
        self.pushButton_2.setText(QCoreApplication.translate("StyleWidget", u"Show", None))
        self.pushButton.setText(QCoreApplication.translate("StyleWidget", u"Enable", None))
        self.close.setText(QCoreApplication.translate("StyleWidget", u"Close", None))
    # retranslateUi
