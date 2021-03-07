# -*- coding: utf-8 -*-
from Qt.QtCore import QObject
from Qt.QtWidgets import QMessageBox
from Qt.QtSql import QSqlDatabase, QSqlQuery


def createConnection():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")
    if not db.open():
        QMessageBox.critical(
            None,
            QObject.tr("Cannot open database"),
            QObject.tr(
                "Unable to establish a database connection.\n"
                "This example needs SQLite support. Please read "
                "the Qt SQL driver documentation for information how "
                "to build it.\n\n"
                "Click Cancel to exit."
            ),
            QMessageBox.Cancel,
        )
        return False

    query = QSqlQuery()
    query.exec_(
        "create table person (id int primary key, "
        "firstname varchar(20), lastname varchar(20))"
    )
    query.exec_("insert into person values(101, 'Danny', 'Young')")
    query.exec_("insert into person values(102, 'Christine', 'Holand')")
    query.exec_("insert into person values(103, 'Lars', 'Gordon')")
    query.exec_("insert into person values(104, 'Roberto', 'Robitaille')")
    query.exec_("insert into person values(105, 'Maria', 'Papadopoulos')")

    query.exec_(
        "create table items (id int primary key,"
        "imagefile int,"
        "itemtype varchar(20),"
        "description varchar(100))"
    )
    query.exec_(
        "insert into items "
        "values(0, 0, 'Qt',"
        "'Qt is a full development framework with tools designed to "
        "streamline the creation of stunning applications and  "
        "amazing user interfaces for desktop, embedded and mobile "
        "platforms.')"
    )
    query.exec_(
        "insert into items "
        "values(1, 1, 'Qt Quick',"
        "'Qt Quick is a collection of techniques designed to help "
        "developers create intuitive, modern-looking, and fluid "
        "user interfaces using a CSS & JavaScript like language.')"
    )
    query.exec_(
        "insert into items "
        "values(2, 2, 'Qt Creator',"
        "'Qt Creator is a powerful cross-platform integrated "
        "development environment (IDE), including UI design tools "
        "and on-device debugging.')"
    )
    query.exec_(
        "insert into items "
        "values(3, 3, 'Qt Project',"
        "'The Qt Project governs the open source development of Qt, "
        "allowing anyone wanting to contribute to join the effort "
        "through a meritocratic structure of approvers and "
        "maintainers.')"
    )

    query.exec_("create table images (itemid int, file varchar(20))")
    query.exec_("insert into images values(0, 'images/qt-logo.png')")
    query.exec_("insert into images values(1, 'images/qt-quick.png')")
    query.exec_("insert into images values(2, 'images/qt-creator.png')")
    query.exec_("insert into images values(3, 'images/qt-project.png')")

    return True
