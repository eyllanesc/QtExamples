from Qt.QtCore import QTimeLine
from Qt.QtGui import QTransform
from Qt.QtWidgets import QGraphicsPixmapItem


class ImageItem(QGraphicsPixmapItem):
    def __init__(self, id_, pixmap, parent=None):
        super().__init__(pixmap, parent)

        self.timeLine = QTimeLine()
        self.recordId = id_
        self.z = 0
        self.setAcceptHoverEvents(True)

        self.timeLine.setDuration(150)
        self.timeLine.setFrameRange(0, 150)

        self.timeLine.frameChanged.connect(self.setFrame)
        self.timeLine.finished.connect(self.updateItemPosition)

        self.adjust()

    def hoverEnterEvent(self, event):

        self.timeLine.setDirection(QTimeLine.Forward)

        if self.z != 1.0:
            self.z = 1.0
            self.updateItemPosition()

        if self.timeLine.state() == QTimeLine.NotRunning:
            self.timeLine.start()

    def hoverLeaveEvent(self, event):
        self.timeLine.setDirection(QTimeLine.Backward)
        if self.z != 0.0:
            self.z = 0.0

        if self.timeLine.state() == QTimeLine.NotRunning:
            self.timeLine.start()

    def setFrame(self, frame):
        self.adjust()
        center = self.boundingRect().center()

        self.setTransform(QTransform.fromTranslate(center.x(), center.y()), True)
        self.setTransform(
            QTransform.fromScale(1 + frame / 330.0, 1 + frame / 330.0), True
        )
        self.setTransform(QTransform.fromTranslate(-center.x(), -center.y()), True)

    def adjust(self):
        if self.boundingRect().height() <= 0:
            return
        self.setTransform(
            QTransform.fromScale(
                120 / self.boundingRect().width(), 120 / self.boundingRect().height()
            )
        )

    def id(self):
        return self.recordId

    def updateItemPosition(self):
        self.setZValue(self.z)
