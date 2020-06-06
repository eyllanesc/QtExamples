import math
import typing

from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QObject,
    QPoint,
    QPointF,
    QRect,
    QStandardPaths,
    Qt,
    QUrl,
)
from PyQt5.QtGui import QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import (
    QNetworkAccessManager,
    QNetworkDiskCache,
    QNetworkReply,
    QNetworkRequest,
)


def qHash(p: QPoint) -> int:
    return p.x() * (17 ^ p.y())


QPointH = type("QPoint", (QPoint,), {"__hash__": qHash})


tdim = 256


def tileForCoordinate(lat: float, lng: float, zoom: int) -> QPointF:
    radianLat = math.radians(lat)
    zn = float(1 << zoom)
    tx = (lng + 180.0) / 360.0
    ty = 0.5 - math.log(math.tan(radianLat) + 1.0 / math.cos(radianLat)) / math.pi / 2.0
    return QPointF(tx * zn, ty * zn)


def longitudeFromTile(tx: float, zoom: int) -> float:
    zn = float(1 << zoom)
    lat = tx / zn * 360.0 - 180.0
    return lat


def latitudeFromTile(ty: float, zoom: int) -> float:
    zn = float(1 << zoom)
    n = math.pi - 2 * math.pi * ty / zn
    return math.degrees(math.atan(math.sinh(n)))


class SlippyMap(QObject):
    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)

        self.width: int = 400
        self.height: int = 300
        self.zoom: int = 15
        self.latitude: float = 59.9138204
        self.longitude: float = 10.7387413

        self.m_offset = QPoint()
        self.m_tilesRect = QRect()

        self.m_emptyTile = QPixmap(tdim, tdim)
        self.m_emptyTile.fill(Qt.lightGray)

        self.m_tilePixmaps: typing.Dict[QPointH, QPixmap] = dict()
        self.m_manager = QNetworkAccessManager()
        self.m_url = QUrl()

        cache = QNetworkDiskCache()
        cache.setCacheDirectory(
            QStandardPaths.writableLocation(QStandardPaths.CacheLocation)
        )
        self.m_manager.setCache(cache)
        self.m_manager.finished.connect(self.handleNetworkData)

    def invalidate(self) -> None:
        if self.width <= 0 or self.height <= 0:
            return

        ct = tileForCoordinate(self.latitude, self.longitude, self.zoom)
        tx = ct.x()
        ty = ct.y()

        # top-left corner of the center tile
        xp = self.width / 2 - (tx - math.floor(tx)) * tdim
        yp = self.height / 2 - (ty - math.floor(ty)) * tdim

        xa = (xp + tdim - 1) / tdim
        ya = (yp + tdim - 1) / tdim
        xs = int(tx) - xa
        ys = int(ty) - ya

        # offset for top-left tile
        self.m_offset = QPoint(xp - xa * tdim, yp - ya * tdim)

        # last tile vertical and horizontal
        xe = int(tx) + (self.width - xp - 1) / tdim
        ye = int(ty) + (self.height - yp - 1) / tdim

        # build a rect
        self.m_tilesRect = QRect(xs, ys, xe - xs + 1, ye - ys + 1)

        if self.m_url.isEmpty():
            self.download()

        self.updated.emit(QRect(0, 0, self.width, self.height))

    def render(self, painter: QPainter, rect: QRect) -> None:
        for x in range(self.m_tilesRect.width() + 1):
            for y in range(self.m_tilesRect.height() + 1):
                tp = QPoint(x + self.m_tilesRect.left(), y + self.m_tilesRect.top())
                box = self.tileRect(tp)
                if rect.intersects(box):
                    painter.drawPixmap(
                        box, self.m_tilePixmaps.get(QPointH(tp), self.m_emptyTile)
                    )

    def pan(self, delta: QPoint) -> None:
        dx = QPointF(delta) / float(tdim)
        center = tileForCoordinate(self.latitude, self.longitude, self.zoom) - dx
        self.latitude = latitudeFromTile(center.y(), self.zoom)
        self.longitude = longitudeFromTile(center.x(), self.zoom)
        self.invalidate()

    updated = pyqtSignal(QRect)

    @pyqtSlot(QNetworkReply)
    def handleNetworkData(self, reply: QNetworkReply) -> None:
        img = QImage()
        tp = reply.request().attribute(QNetworkRequest.User)
        if not reply.error():
            if not img.load(reply, ""):
                img = QImage()
        reply.deleteLater()
        self.m_tilePixmaps[QPointH(tp)] = (
            self.m_emptyTile if img.isNull() else QPixmap.fromImage(img)
        )
        self.updated.emit(self.tileRect(tp))

        # purge unused spaces
        bound = self.m_tilesRect.adjusted(-2, -2, 2, 2)
        self.m_tilePixmaps = {
            tp: pixmap
            for tp, pixmap in self.m_tilePixmaps.items()
            if bound.contains(tp)
        }

        self.download()

    @pyqtSlot()
    def download(self):
        grab = QPoint(0, 0)
        for x in range(self.m_tilesRect.width() + 1):
            for y in range(self.m_tilesRect.height() + 1):
                tp = self.m_tilesRect.topLeft() + QPoint(x, y)
                if QPointH(tp) not in self.m_tilePixmaps:
                    grab = tp
                    break

        if grab == QPoint(0, 0):
            self.m_url = QUrl()
            return
        path = "http://tile.openstreetmap.org/%d/%d/%d.png"
        self.m_url = QUrl(path % (self.zoom, grab.x(), grab.y()))
        request = QNetworkRequest()
        request.setUrl(self.m_url)
        request.setRawHeader(b"User-Agent", b"The Qt Company (Qt) Graphics Dojo 1.0")
        request.setAttribute(QNetworkRequest.User, grab)
        self.m_manager.get(request)

    def tileRect(self, tp: QPoint):
        t = tp - self.m_tilesRect.topLeft()
        x = t.x() * tdim + self.m_offset.x()
        y = t.y() * tdim + self.m_offset.y()
        return QRect(x, y, tdim, tdim)
