# -*- coding: utf-8 -*-
from Qt.QtChart import QChart, QLineSeries, QSplineSeries
from Qt.QtCore import QPoint, QRect, QRectF, QSizeF, Qt
from Qt.QtGui import QPainter
from Qt.QtWidgets import QGraphicsScene, QGraphicsSimpleTextItem, QGraphicsView

from callout import Callout


class View(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        scene = QGraphicsScene(self)
        self.setScene(scene)
        self.m_tooltip = None
        self.m_callouts = []

        self.setDragMode(QGraphicsView.NoDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # chart
        self.m_chart = QChart()
        self.m_chart.setMinimumSize(640, 480)
        self.m_chart.setTitle(
            "Hover the line to show callout. Click the line to make it stay"
        )
        self.m_chart.legend().hide()
        series = QLineSeries()
        series.append(1, 3)
        series.append(4, 5)
        series.append(5, 4.5)
        series.append(7, 1)
        series.append(11, 2)
        self.m_chart.addSeries(series)

        series2 = QSplineSeries()
        series2.append(1.6, 1.4)
        series2.append(2.4, 3.5)
        series2.append(3.7, 2.5)
        series2.append(7, 4)
        series2.append(10, 2)
        self.m_chart.addSeries(series2)

        self.m_chart.createDefaultAxes()
        self.m_chart.setAcceptHoverEvents(True)

        self.setRenderHint(QPainter.Antialiasing)
        self.scene().addItem(self.m_chart)

        self.m_coordX = QGraphicsSimpleTextItem(self.m_chart)
        self.m_coordX.setPos(
            self.m_chart.size().width() / 2 - 50, self.m_chart.size().height()
        )
        self.m_coordX.setText("X: ")
        self.m_coordY = QGraphicsSimpleTextItem(self.m_chart)
        self.m_coordY.setPos(
            self.m_chart.size().width() / 2 + 50, self.m_chart.size().height()
        )
        self.m_coordY.setText("Y: ")

        series.clicked.connect(self.keepCallout)
        series.hovered.connect(self.tooltip)

        series2.clicked.connect(self.keepCallout)
        series2.hovered.connect(self.tooltip)

        self.setMouseTracking(True)

    def resizeEvent(self, event):
        if self.scene() is not None:
            self.scene().setSceneRect(QRectF(QRect(QPoint(0, 0), event.size())))
            self.m_chart.resize(QSizeF(event.size()))
            self.m_coordX.setPos(
                self.m_chart.size().width() / 2 - 50, self.m_chart.size().height() - 20
            )
            self.m_coordY.setPos(
                self.m_chart.size().width() / 2 + 50, self.m_chart.size().height() - 20
            )
            for callout in self.m_callouts:
                callout.updateGeometry()
        super().resizeEvent(event)

    def mouseMoveEvent(self, event):
        self.m_coordX.setText("X: %f" % self.m_chart.mapToValue(event.pos()).x())
        self.m_coordY.setText("Y: %f" % self.m_chart.mapToValue(event.pos()).y())
        super().mouseMoveEvent(event)

    def keepCallout(self):
        self.m_callouts.append(self.m_tooltip)
        self.m_tooltip = Callout(self.m_chart)

    def tooltip(self, point, state):
        if self.m_tooltip is None:
            self.m_tooltip = Callout(self.m_chart)

        if state:
            self.m_tooltip.setText("X: {:f} \nY: {:f} ".format(point.x(), point.y()))
            self.m_tooltip.setAnchor(point)
            self.m_tooltip.setZValue(11)
            self.m_tooltip.updateGeometry()
            self.m_tooltip.show()
        else:
            self.m_tooltip.hide()
