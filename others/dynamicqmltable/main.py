from dataclasses import dataclass, fields
import os
import os.path
import random
import sys
from typing import Any, Dict, List, Optional

from PySide2.QtCore import (
    Property,
    QAbstractTableModel,
    QByteArray,
    QCoreApplication,
    QModelIndex,
    QObject,
    Qt,
    QUrl,
    Slot,
)
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


@dataclass
class Item:
    checked: bool = False
    name: str = ""
    x: int = 0
    y: int = 0


class TableItem(QAbstractTableModel):
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._data = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(fields(Item))

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if (
            0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
        ):
            instance = self._data[index.row()]
            value = None
            fs = fields(Item)
            if role == Qt.DisplayRole:
                name = fs[index.column()].name
                value = getattr(instance, name)
            if role >= Qt.UserRole:
                ix = role - Qt.UserRole
                name = fs[ix].name
                value = getattr(instance, name)
            return value

    @Slot(str, int, int, result=bool)
    @Slot(str, int, int, bool, result=bool)
    def append_row(self, name: str, x: int, y: int, checked: bool = False) -> bool:
        item = Item(checked=checked, name=name, x=x, y=y)
        return self.append_item(item)

    def append_item(self, item: Item) -> bool:
        if not isinstance(item, Item):
            return False
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(item)
        self.endInsertRows()
        return True

    @Slot(result="QVariantList")
    def names(self) -> List[str]:
        return [f.name for f in fields(Item)]

    def roleNames(self) -> Dict[int, QByteArray]:
        d = dict()
        d[Qt.DisplayRole] = QByteArray(b"display")
        for i, field in enumerate(fields(Item), start=Qt.UserRole):
            d[i] = QByteArray(field.name.encode())
        return d

    @Slot(int, bool, result=bool)
    def setChecked(self, row: int, state: bool) -> bool:
        if 0 <= row <= self.rowCount():
            item = self._data[row]
            if item.checked != state:
                item.checked = state
                self.dataChanged.emit(
                    self.index(row, 0), self.index(row, self.columnCount() - 1)
                )
            return True
        return False


class Manager(QObject):
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._model = TableItem()

    model = Property(QObject, fget=lambda instance: instance._model, constant=True)


def main():
    app = QGuiApplication(sys.argv)

    manager = Manager()

    for i in range(200):
        manager.model.append_item(
            Item(
                name=f"name{i}",
                checked=i % 2 == 0,
                x=random.randint(-100, 100),
                y=random.randint(0, 100),
            )
        )

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("manager", manager)

    filename = os.path.join(CURRENT_DIR, "main.qml")
    url = QUrl.fromLocalFile(filename)

    def handle_object_created(obj, objUrl):
        if not obj and url == objUrl:
            QCoreApplication.exit(-1)

    engine.objectCreated.connect(handle_object_created, Qt.QueuedConnection)
    engine.load(url)

    ret = app.exec_()
    sys.exit(ret)


if __name__ == "__main__":
    main()
