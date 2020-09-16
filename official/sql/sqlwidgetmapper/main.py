from qtpy import QtWidgets, QtSql


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupModel()

        self.nameLabel = QtWidgets.QLabel(self.tr("Na&me:"))
        self.nameEdit = QtWidgets.QLineEdit()
        self.addressLabel = QtWidgets.QLabel(self.tr("&Address:"))
        self.addressEdit = QtWidgets.QTextEdit()
        self.typeLabel = QtWidgets.QLabel(self.tr("&Type:"))
        self.typeComboBox = QtWidgets.QComboBox()
        self.nextButton = QtWidgets.QPushButton(self.tr("&Next"))
        self.previousButton = QtWidgets.QPushButton(self.tr("&Previous"))

        self.nameLabel.setBuddy(self.nameEdit)
        self.addressLabel.setBuddy(self.addressEdit)
        self.typeLabel.setBuddy(self.typeComboBox)

        relModel = self.model.relationModel(self.typeIndex)
        self.typeComboBox.setModel(relModel)
        self.typeComboBox.setModelColumn(relModel.fieldIndex("description"))

        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QtSql.QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.nameEdit, self.model.fieldIndex("name"))
        self.mapper.addMapping(self.addressEdit, self.model.fieldIndex("address"))
        self.mapper.addMapping(self.typeComboBox, self.typeIndex)

        self.previousButton.clicked.connect(self.mapper.toPrevious)
        self.nextButton.clicked.connect(self.mapper.toNext)
        self.mapper.currentIndexChanged.connect(self.updateButtons)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.nameLabel, 0, 0, 1, 1)
        layout.addWidget(self.nameEdit, 0, 1, 1, 1)
        layout.addWidget(self.previousButton, 0, 2, 1, 1)
        layout.addWidget(self.addressLabel, 1, 0, 1, 1)
        layout.addWidget(self.addressEdit, 1, 1, 2, 1)
        layout.addWidget(self.nextButton, 1, 2, 1, 1)
        layout.addWidget(self.typeLabel, 3, 0, 1, 1)
        layout.addWidget(self.typeComboBox, 3, 1, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("SQL Widget Mapper"))
        self.mapper.toFirst()

    def setupModel(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(":memory:")
        if not db.open():
            QtWidgets.QMessageBox.critical(
                None,
                self.tr("Cannot open database"),
                self.tr(
                    "Unable to establish a database connection.\n"
                    "This example needs SQLite support. Please read "
                    "the Qt SQL driver documentation for information how "
                    "to build it."
                ),
                QtWidgets.QMessageBox.Cancel,
            )
            return

        query = QtSql.QSqlQuery()
        query.exec(
            "create table person (id int primary key, "
            "name varchar(20), address varchar(200), typeid int)"
        )
        query.exec(
            "insert into person values(1, 'Alice', "
            "'<qt>123 Main Street<br/>Market Town</qt>', 101)"
        )
        query.exec(
            "insert into person values(2, 'Bob', "
            "'<qt>PO Box 32<br/>Mail Handling Service"
            "<br/>Service City</qt>', 102)"
        )
        query.exec(
            "insert into person values(3, 'Carol', "
            "'<qt>The Lighthouse<br/>Remote Island</qt>', 103)"
        )
        query.exec(
            "insert into person values(4, 'Donald', "
            "'<qt>47338 Park Avenue<br/>Big City</qt>', 101)"
        )
        query.exec(
            "insert into person values(5, 'Emma', "
            "'<qt>Research Station<br/>Base Camp<br/>"
            "Big Mountain</qt>', 103)"
        )

        query.exec("create table addresstype (id int, description varchar(20))")
        query.exec("insert into addresstype values(101, 'Home')")
        query.exec("insert into addresstype values(102, 'Work')")
        query.exec("insert into addresstype values(103, 'Other')")

        self.model = QtSql.QSqlRelationalTableModel(self)
        self.model.setTable("person")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)

        self.typeIndex = self.model.fieldIndex("typeid")

        self.model.setRelation(
            self.typeIndex, QtSql.QSqlRelation("addresstype", "id", "description")
        )
        self.model.select()

    def updateButtons(self, row):
        self.previousButton.setEnabled(row > 0)
        self.nextButton.setEnabled(row < self.model.rowCount() - 1)


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
