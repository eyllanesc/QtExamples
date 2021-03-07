# -*- coding: utf-8 -*-
from Qt.QtCore import Qt
from Qt.QtWidgets import (
    QDialogButtonBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableView,
    QWidget,
)
from Qt.QtSql import QSqlTableModel


class TableEditor(QWidget):
    def __init__(self, tableName, parent=None):
        super().__init__(parent)
        self.model = QSqlTableModel(self)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, self.tr("ID"))
        self.model.setHeaderData(1, Qt.Horizontal, self.tr("First name"))
        self.model.setHeaderData(2, Qt.Horizontal, self.tr("Last name"))

        view = QTableView()
        view.setModel(self.model)
        view.resizeColumnsToContents()

        self.submitButton = QPushButton(self.tr("Submit"))
        self.submitButton.setDefault(True)
        self.revertButton = QPushButton(self.tr("&Revert"))
        self.quitButton = QPushButton(self.tr("Quit"))

        self.buttonBox = QDialogButtonBox(Qt.Vertical)
        self.buttonBox.addButton(self.submitButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.revertButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.quitButton, QDialogButtonBox.RejectRole)

        self.submitButton.clicked.connect(self.submit)
        self.revertButton.clicked.connect(self.model.revertAll)
        self.quitButton.clicked.connect(self.close)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(view)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Cached Table"))

    def submit(self):
        self.model.database().transaction()
        if self.model.submitAll():
            self.model.database().commit()
        else:
            self.model.database().rollback()
            QMessageBox.warning(
                self,
                self.tr("Cached Table"),
                self.tr(
                    "The database reported an error: {}".format(
                        self.model.lastError().text()
                    )
                ),
            )
