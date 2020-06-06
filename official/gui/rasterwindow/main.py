from PyQt5.QtCore import QEvent, QRect, QRectF, Qt
from PyQt5.QtGui import (
    QBackingStore,
    QExposeEvent,
    QGuiApplication,
    QGradient,
    QPaintDevice,
    QPainter,
    QRegion,
    QResizeEvent,
    QWindow,
)


class RasterWindow(QWindow):
    def __init__(self, parent: QWindow = None) -> None:
        super().__init__(parent)
        self.m_backingStore = QBackingStore(self)
        self.setGeometry(100, 100, 300, 200)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.UpdateRequest:
            self.renderNow()
            return True
        return super().event(event)

    def renderLater(self) -> None:
        self.requestUpdate()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.m_backingStore.resize(event.size())

    def exposeEvent(self, event: QExposeEvent) -> None:
        if self.isExposed():
            self.renderNow()

    def renderNow(self) -> None:
        if not self.isExposed():
            return

        rect = QRect(0, 0, self.width(), self.height())
        self.m_backingStore.beginPaint(QRegion(rect))

        device: QPaintDevice = self.m_backingStore.paintDevice()
        painter = QPainter(device)

        painter.fillRect(0, 0, self.width(), self.height(), QGradient.NightFade)
        self.render(painter)
        painter.end()

        self.m_backingStore.endPaint()
        self.m_backingStore.flush(QRegion(rect))

    def render(self, painter: QPainter) -> None:
        painter.drawText(
            QRectF(0, 0, self.width(), self.height()), Qt.AlignCenter, "QWindow"
        )


def main():
    import sys

    app = QGuiApplication(sys.argv)
    w = RasterWindow()
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
