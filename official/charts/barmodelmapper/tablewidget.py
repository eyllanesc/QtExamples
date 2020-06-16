from PyQt5.QtChart import (QBarCategoryAxis, QBarSeries, QChart, QChartView,
                           QValueAxis, QVBarModelMapper)
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGridLayout, QHeaderView, QTableView, QWidget

from customtablemodel import CustomTableModel


class TableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_model = CustomTableModel()

        tableView = QTableView()
        tableView.setModel(self.m_model)
        tableView.setMinimumWidth(300)
        tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.m_model.setParent(tableView)

        chart = QChart()
        chart.setAnimationOptions(QChart.AllAnimations)

        series = QBarSeries()

        first = 3
        count = 5
        mapper = QVBarModelMapper(self)
        mapper.setFirstBarSetColumn(1)
        mapper.setLastBarSetColumn(4)
        mapper.setFirstRow(first)
        mapper.setRowCount(count)
        mapper.setSeries(series)
        mapper.setModel(self.m_model)
        chart.addSeries(series)

        seriesColorHex = "#000000"

        barsets = series.barSets()
        for i, barset in enumerate(barsets):
            seriesColorHex = barset.brush().color().name()
            self.m_model.addMapping(
                seriesColorHex, QRect(1 + i, first, 1, barset.count())
            )

        categories = ("April", "May", "June", "July", "August")
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        axisY = QValueAxis()
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setMinimumSize(640, 480)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(tableView, 1, 0)
        mainLayout.addWidget(chartView, 1, 1)
        mainLayout.setColumnStretch(1, 1)
        mainLayout.setColumnStretch(0, 0)
