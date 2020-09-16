from Qt.QtCore import QPoint, QPointF
from Qt.QtGui import QColor, QLinearGradient, QPixmap
from Qt.QtWidgets import QGraphicsScene, QGraphicsView
from Qt.QtSql import QSqlRelation, QSqlRelationalTableModel

from imageitem import ImageItem
from informationwindow import InformationWindow


class View(QGraphicsView):
    def __init__(self, items, images, parent=None):
        super().__init__(parent)
        self.informationWindows = []
        self.itemTable = QSqlRelationalTableModel(self)
        self.itemTable.setTable(items)
        self.itemTable.setRelation(1, QSqlRelation(images, "itemid", "file"))
        self.itemTable.select()

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 465, 365)
        self.setScene(self.scene)

        self.addItems()

        self.setMinimumSize(470, 370)
        self.setMaximumSize(470, 370)

        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 370))
        gradient.setColorAt(0, QColor("#868482"))
        gradient.setColorAt(1, QColor("#5d5b59"))
        self.setBackgroundBrush(gradient)

    def addItems(self):

        itemCount = self.itemTable.rowCount()

        imageOffset = 150
        leftMargin = 70
        topMargin = 40

        for i in range(itemCount):
            record = self.itemTable.record(i)

            id_ = record.value("id")
            file = record.value("file")
            item = record.value("itemtype")

            columnOffset = (i % 2) * 37
            x = ((i % 2) * imageOffset) + leftMargin + columnOffset
            y = ((i / 2) * imageOffset) + topMargin

            image = ImageItem(id_, QPixmap(":/" + file))
            image.setData(0, i)
            image.setPos(x, y)
            self.scene.addItem(image)

            label = self.scene.addText(item)
            label.setDefaultTextColor(QColor("#d7d6d5"))
            labelOffset = QPointF((120 - label.boundingRect().width()) / 2, 120.0)
            label.setPos(QPointF(x, y) + labelOffset)

    def mouseReleaseEvent(self, event):
        if item := self.itemAt(event.pos()):
            if isinstance(item, ImageItem):
                self.showInformation(item)
        super().mouseReleaseEvent(event)

    def showInformation(self, image):
        id_ = image.id()
        if id_ < 0 or id_ >= self.itemTable.rowCount():
            return

        window = self.findWindow(id_)
        if not window:
            window = InformationWindow(id_, self.itemTable, self)
            window.imageChanged.connect(self.updateImage)
            window.move(self.pos() + QPoint(20, 40))
            window.show()
            self.informationWindows.append(window)

        if window.isVisible():
            window.raise_()
            window.activateWindow()
        else:
            window.show()

    def updateImage(self, id_, fileName):
        items = self.scene.items()

        for item in items:
            if isinstance(item, ImageItem):
                if item.id() == id_:
                    item.setPixmap(QPixmap(":/" + fileName))
                    item.adjust()
                    break

    def findWindow(self, id_):
        for window in self.informationWindows:
            if window and window.id() == id_:
                return window
