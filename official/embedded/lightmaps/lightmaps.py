from PyQt5.QtCore import pyqtSlot, QBasicTimer, QPoint, QRect, QSize, Qt, QTimerEvent
from PyQt5.QtGui import (
    QColor,
    QKeyEvent,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPixmap,
    QRadialGradient,
    QResizeEvent,
)
from PyQt5.QtWidgets import QWidget

from slippymap import SlippyMap

# how long (milliseconds) the user need to hold (after a tap on the screen)
# before triggering the magnifying glass feature
# 701, a prime number, is the sum of 229, 233, 239
# (all three are also prime numbers, consecutive!)
HOLD_TIME = 701

# maximum size of the magnifier
# Hint: see above to find why I picked this one :)
MAX_MAGNIFIER = 229


class LightMaps(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.m_normalMap = SlippyMap(self)
        self.m_largeMap = SlippyMap(self)
        self.m_normalMap.updated.connect(self.updateMap)
        self.m_largeMap.updated.connect(self.update)
        self.pressed = False
        self.snapped = False
        self.pressPos = QPoint()
        self.dragPos = QPoint()
        self.tapTimer = QBasicTimer()
        self.zoomed = False
        self.zoomPixmap = QPixmap()
        self.maskPixmap = QPixmap()
        self.invert = False

    def setCenter(self, lat: float, lng: float):
        self.m_normalMap.latitude = lat
        self.m_normalMap.longitude = lng
        self.m_normalMap.invalidate()
        self.m_largeMap.latitude = lat
        self.m_largeMap.longitude = lng
        self.m_largeMap.invalidate()

    @pyqtSlot()
    def toggleNightMode(self) -> None:
        self.invert = not self.invert
        self.update()

    def activateZoom(self) -> None:
        self.zoomed = True
        self.tapTimer.stop()
        self.m_largeMap.zoom = self.m_normalMap.zoom + 1
        self.m_largeMap.width = self.m_normalMap.width * 2
        self.m_largeMap.height = self.m_normalMap.height * 2
        self.m_largeMap.latitude = self.m_normalMap.latitude
        self.m_largeMap.longitude = self.m_normalMap.longitude
        self.m_largeMap.invalidate()
        self.update()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.m_normalMap.width = self.width()
        self.m_normalMap.height = self.height()
        self.m_normalMap.invalidate()
        self.m_largeMap.width = self.m_normalMap.width * 2
        self.m_largeMap.height = self.m_normalMap.height * 2
        self.m_largeMap.invalidate()

    def paintEvent(self, event: QPaintEvent) -> None:
        p = QPainter(self)
        self.m_normalMap.render(p, event.rect())
        p.setPen(Qt.black)
        p.drawText(
            self.rect(),
            Qt.AlignBottom | Qt.TextWordWrap,
            "Map data CCBYSA 2009 OpenStreetMap.org contributors",
        )
        p.end()

        if self.zoomed:
            dim = min(self.width(), self.height())
            magnifierSize = min(MAX_MAGNIFIER, dim * 2 / 3)
            radius = magnifierSize / 2
            ring = radius - 15
            box = QSize(magnifierSize, magnifierSize)

            if self.maskPixmap.size() != box:
                self.maskPixmap = QPixmap(box)
                self.maskPixmap.fill(Qt.transparent)

                g = QRadialGradient()
                g.setCenter(radius, radius)
                g.setFocalPoint(radius, radius)
                g.setRadius(radius)
                g.setColorAt(1.0, QColor(255, 255, 255, 0))
                g.setColorAt(0.5, QColor(128, 128, 128, 255))

                mask = QPainter(self.maskPixmap)
                mask.setRenderHint(QPainter.Antialiasing)
                mask.setCompositionMode(QPainter.CompositionMode_Source)
                mask.setBrush(g)
                mask.setPen(Qt.NoPen)
                mask.drawRect(self.maskPixmap.rect())
                mask.setBrush(QColor(Qt.transparent))
                mask.drawEllipse(g.center(), ring, ring)
                mask.end()

            center = self.dragPos - QPoint(0, radius)
            center = center + QPoint(0, radius / 2)
            corner = center - QPoint(radius, radius)

            xy = center * 2 - QPoint(radius, radius)

            # only set the dimension to the magnified portion
            if self.zoomPixmap.size() != box:
                zoomPixmap = QPixmap(box)
                zoomPixmap.fill(Qt.lightGray)

            if True:
                p = QPainter(zoomPixmap)
                p.translate(-xy)
                self.m_largeMap.render(p, QRect(xy, box))
                p.end()

            clipPath = QPainterPath()
            clipPath.addEllipse(center, ring, ring)

            p = QPainter(self)
            p.setRenderHint(QPainter.Antialiasing)
            p.setClipPath(clipPath)
            p.drawPixmap(corner, zoomPixmap)
            p.setClipping(False)
            p.drawPixmap(corner, self.maskPixmap)
            p.setPen(Qt.gray)
            p.drawPath(clipPath)
        if self.invert:
            p = QPainter(self)
            p.setCompositionMode(QPainter.CompositionMode_Difference)
            p.fillRect(event.rect(), Qt.white)
            p.end()

    def timerEvent(self, event: QTimerEvent) -> None:
        if not self.zoomed:
            self.activateZoom()
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() != Qt.LeftButton:
            return
        self.pressed = self.snapped = True
        self.pressPos = self.dragPos = event.pos()
        self.tapTimer.stop()
        self.tapTimer.start(HOLD_TIME, self)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not event.buttons():
            return
        if not self.zoomed:
            if not self.pressed or not self.snapped:
                delta = event.pos() - self.pressPos
                self.pressPos = event.pos()
                self.m_normalMap.pan(delta)
                return
            else:
                threshold = 10
                delta = event.pos() - self.pressPos
                if self.snapped:
                    self.snapped &= delta.x() < threshold
                    self.snapped &= delta.y() < threshold
                    self.snapped &= delta.x() > -threshold
                    self.snapped &= delta.y() > -threshold
                if not self.snapped:
                    self.tapTimer.stop()
        else:
            self.dragPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.zoomed = False
        self.update()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.zoomed:
            if event.key() == Qt.Key_Left:
                self.m_normalMap.pan(QPoint(20, 0))
            if event.key() == Qt.Key_Right:
                self.m_normalMap.pan(QPoint(-20, 0))
            if event.key() == Qt.Key_Up:
                self.m_normalMap.pan(QPoint(0, 20))
            if event.key() == Qt.Key_Down:
                self.m_normalMap.pan(QPoint(0, -20))
            if event.key() == Qt.Key_Z or event.key() == Qt.Key_Select:
                self.dragPos = QPoint(self.width() / 2, self.height() / 2)
                self.activateZoom()
        else:
            if event.key() == Qt.Key_Z or event.key() == Qt.Key_Select:
                self.zoomed = False
                self.update()
            delta = QPoint(0, 0)
            if event.key() == Qt.Key_Left:
                delta = QPoint(-15, 0)
            if event.key() == Qt.Key_Right:
                delta = QPoint(15, 0)
            if event.key() == Qt.Key_Up:
                delta = QPoint(0, -15)
            if event.key() == Qt.Key_Down:
                delta = QPoint(0, 15)
            if delta != QPoint(0, 0):
                self.dragPos += delta
                self.update()

    @pyqtSlot(QRect)
    def updateMap(self, r):
        self.update(r)
