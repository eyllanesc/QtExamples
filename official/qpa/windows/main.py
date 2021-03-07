# -*- coding: utf-8 -*-
from qtpy.QtCore import QPoint, QRect, QSize, Qt
from qtpy.QtGui import (
    QBackingStore,
    QColor,
    QFont,
    QGuiApplication,
    QImage,
    QPainter,
    QRegion,
    QWindow,
)

colorIndexId = 0

colorTable = (QColor("#f09f8f"), QColor("#a2bff2"), QColor("#c0ef8f"))


class Window(QWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        global colorIndexId
        colorIndexId += 1
        self.m_backgroundColorIndex = colorIndexId

        self.m_text = ""
        self.m_image = QImage()
        self.m_lastPos = QPoint()
        self.m_backingStore = None
        self.m_renderTimer = 0

        self.initialize()

    def mousePressEvent(self, event):
        self.m_lastPos = event.pos()

    def mouseMoveEvent(self, event):
        if self.m_lastPos != QPoint(-1, -1):
            p = QPainter(self.m_image)
            p.setRenderHint(QPainter.Antialiasing)
            p.drawLine(self.m_lastPos, event.pos())
            self.m_lastPos = event.pos()

            self.scheduleRender()

    def mouseReleaseEvent(self, event):
        if self.m_lastPos != QPoint(-1, -1):
            p = QPainter(self.m_image)
            p.setRenderHint(QPainter.Antialiasing)
            p.drawLine(self.m_lastPos, event.pos())
            self.m_lastPos = QPoint(-1, -1)

            self.scheduleRender()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            if len(self.m_text) > 1:
                self.m_text = self.m_text[:-1]
        elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.m_text += "\n"
        else:
            self.m_text += event.text()
        self.scheduleRender()

    def exposeEvent(self, event):
        self.scheduleRender()

    def resizeEvent(self, event):
        old = QImage(self.m_image)

        width = max(self.geometry().width(), old.width())
        height = max(self.geometry().height(), old.height())

        if width > old.width() or height > old.height():
            self.m_image = QImage(width, height, QImage.Format_RGB32)
            self.m_image.fill(
                colorTable[self.m_backgroundColorIndex % len(colorTable)].rgba()
            )
            p = QPainter(self.m_image)
            p.drawImage(0, 0, old)

        self.scheduleRender()

    def timerEvent(self, event):
        if self.isExposed():
            self.render()
        self.killTimer(self.m_renderTimer)
        self.m_renderTimer = 0

    def render(self):
        rect = QRect(QPoint(), self.geometry().size())
        self.m_backingStore.resize(rect.size())

        self.m_backingStore.beginPaint(QRegion(rect))

        device = self.m_backingStore.paintDevice()

        p = QPainter(device)
        p.drawImage(0, 0, self.m_image)

        font = QFont()
        font.setPixelSize(32)

        p.setFont(font)
        p.drawText(rect, 0, self.m_text)

        self.m_backingStore.endPaint()
        self.m_backingStore.flush(QRegion(rect))

    def scheduleRender(self):
        if not self.m_renderTimer:
            self.m_renderTimer = self.startTimer(1)

    def initialize(self):
        if self.parent():
            self.setGeometry(QRect(160, 120, 320, 240))
        else:
            self.setFlags(
                self.flags()
                | Qt.WindowTitleHint
                | Qt.WindowSystemMenuHint
                | Qt.WindowMinMaxButtonsHint
                | Qt.WindowCloseButtonHint
            )
            baseSize = QSize(640, 480)
            self.setGeometry(QRect(self.geometry().topLeft(), baseSize))

            self.setSizeIncrement(QSize(10, 10))
            self.setBaseSize(baseSize)
            self.setMinimumSize(QSize(240, 160))
            self.setMaximumSize(QSize(800, 600))

        self.create()
        self.m_backingStore = QBackingStore(self)

        self.m_image = QImage(self.geometry().size(), QImage.Format_RGB32)
        self.m_image.fill(
            colorTable[self.m_backgroundColorIndex % len(colorTable)].rgba()
        )

        self.m_lastPos = QPoint(-1, -1)
        self.m_renderTimer = 0


def main():
    import sys

    app = QGuiApplication(sys.argv)

    a = Window()
    a.setFramePosition(QPoint(10, 10))
    a.setTitle("Window A")
    a.setObjectName(a.title())
    a.setVisible(True)

    b = Window()
    b.setFramePosition(QPoint(100, 100))
    b.setTitle("Window B")
    b.setObjectName(b.title())
    b.setVisible(True)

    child = Window(b)
    child.setObjectName("ChildOfB")
    child.setVisible(True)

    windows = []
    screens = app.screens()
    for screen in screens:
        if screen == app.primaryScreen():
            continue
        window = Window(screen)
        geometry = window.geometry()
        geometry.moveCenter(screen.availableGeometry().center())
        window.setGeometry(geometry)
        window.setVisible(True)
        window.setTitle(screen.name())
        window.setObjectName(window.title())
        windows.append(window)

    return app.exec()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
