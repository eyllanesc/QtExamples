from Qt.QtCore import QPoint, QPointF, QRect, QRectF, Qt
from Qt.QtGui import QColor, QFont, QFontMetrics, QPainterPath
from Qt.QtWidgets import QGraphicsItem


class Callout(QGraphicsItem):
    def __init__(self, chart):
        super().__init__(chart)

        self.m_chart = chart
        self.m_text = ""
        self.m_textRect = QRectF()
        self.m_rect = QRectF()
        self.m_anchor = QPointF()
        self.m_font = QFont()

    def boundingRect(self):
        anchor = self.mapFromParent(self.m_chart.mapToPosition(self.m_anchor))
        rect = QRectF()
        rect.setLeft(min(self.m_rect.left(), anchor.x()))
        rect.setRight(max(self.m_rect.right(), anchor.x()))
        rect.setTop(min(self.m_rect.top(), anchor.y()))
        rect.setBottom(max(self.m_rect.bottom(), anchor.y()))
        return rect

    def paint(self, painter, option, widget=None):
        path = QPainterPath()
        path.addRoundedRect(self.m_rect, 5, 5)

        anchor = self.mapFromParent(self.m_chart.mapToPosition(self.m_anchor))
        if not self.m_rect.contains(anchor):
            point1 = QPointF()
            point2 = QPointF()

            # establish the position of the anchor point in relation to m_rect
            above = anchor.y() <= self.m_rect.top()
            aboveCenter = (
                anchor.y() > self.m_rect.top()
                and anchor.y() <= self.m_rect.center().y()
            )
            belowCenter = (
                anchor.y() > self.m_rect.center().y()
                and anchor.y() <= self.m_rect.bottom()
            )
            below = anchor.y() > self.m_rect.bottom()

            onLeft = anchor.x() <= self.m_rect.left()
            leftOfCenter = (
                anchor.x() > self.m_rect.left()
                and anchor.x() <= self.m_rect.center().x()
            )
            rightOfCenter = (
                anchor.x() > self.m_rect.center().x()
                and anchor.x() <= self.m_rect.right()
            )
            onRight = anchor.x() > self.m_rect.right()

            # get the nearest m_rect corner.
            x = (onRight + rightOfCenter) * self.m_rect.width()
            y = (below + belowCenter) * self.m_rect.height()
            cornerCase = (
                (above and onLeft)
                or (above and onRight)
                or (below and onLeft)
                or (below and onRight)
            )
            vertical = abs(anchor.x() - x) > abs(anchor.y() - y)

            x1 = (
                x
                + leftOfCenter * 10
                - rightOfCenter * 20
                + cornerCase * int(not vertical) * (onLeft * 10 - onRight * 20)
            )
            y1 = (
                y
                + aboveCenter * 10
                - belowCenter * 20
                + cornerCase * int(vertical) * (above * 10 - below * 20)
            )
            point1.setX(x1)
            point1.setY(y1)

            x2 = (
                x
                + leftOfCenter * 20
                - rightOfCenter * 10
                + cornerCase * int(not vertical) * (onLeft * 20 - onRight * 10)
            )
            y2 = (
                y
                + aboveCenter * 20
                - belowCenter * 10
                + cornerCase * int(vertical) * (above * 20 - below * 10)
            )
            point2.setX(x2)
            point2.setY(y2)

            path.moveTo(point1)
            path.lineTo(anchor)
            path.lineTo(point2)
            path = path.simplified()

        painter.setBrush(QColor(255, 255, 255))
        painter.drawPath(path)
        painter.drawText(self.m_textRect, self.m_text)

    def mousePressEvent(self, event):
        event.setAccepted(True)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.setPos(self.mapToParent(event.pos() - event.buttonDownPos(Qt.LeftButton)))
            event.setAccepted(True)
        else:
            event.setAccepted(False)

    def setText(self, text):
        self.m_text = text
        metrics = QFontMetrics(self.m_font)
        self.m_textRect = QRectF(metrics.boundingRect(
            QRect(0, 0, 150, 150), Qt.AlignLeft, self.m_text
        ))
        self.m_textRect.translate(5, 5)
        self.prepareGeometryChange()
        self.m_rect = self.m_textRect.adjusted(-5, -5, 5, 5)

    def setAnchor(self, point):
        self.m_anchor = point

    def updateGeometry(self):
        self.prepareGeometryChange()
        self.setPos(self.m_chart.mapToPosition(self.m_anchor) + QPoint(10, -50))
