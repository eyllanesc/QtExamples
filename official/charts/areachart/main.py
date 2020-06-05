from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QColor, QGradient, QLinearGradient, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QAreaSeries, QChart, QChartView, QLineSeries


def main():
    import sys

    app = QApplication(sys.argv)

    series0 = QLineSeries()
    series1 = QLineSeries()

    series0 << QPointF(1, 5) << QPointF(3, 7) << QPointF(7, 6) << QPointF(
        9, 7
    ) << QPointF(12, 6) << QPointF(16, 7) << QPointF(18, 5)
    series1 << QPointF(1, 3) << QPointF(3, 4) << QPointF(7, 3) << QPointF(
        8, 2
    ) << QPointF(12, 3) << QPointF(16, 4) << QPointF(18, 3)

    series = QAreaSeries(series0, series1)
    series.setName("Batman")
    pen = QPen(0x059605)
    pen.setWidth(3)
    series.setPen(pen)

    gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
    gradient.setColorAt(0.0, QColor(0x3CC63C))
    gradient.setColorAt(1.0, QColor(0x26F626))
    gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
    series.setBrush(gradient)

    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Simple areachart example")
    chart.createDefaultAxes()
    chart.axes(Qt.Horizontal)[0].setRange(0, 20)
    chart.axes(Qt.Vertical)[0].setRange(0, 10)

    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
