from Qt.QtChart import QCandlestickSeries, QChart, QChartView
from Qt.QtCore import QDateTime, QFile, QIODevice, Qt
from Qt.QtGui import QColor, QPainter
from Qt.QtWidgets import QApplication, QMainWindow

import candlestickdata_rc  # noqa: F401
from candlestickdatareader import CandlestickDataReader


def main():
    import sys

    a = QApplication(sys.argv)

    acmeSeries = QCandlestickSeries()
    acmeSeries.setName("Acme Ltd")
    acmeSeries.setIncreasingColor(QColor(Qt.green))
    acmeSeries.setDecreasingColor(QColor(Qt.red))

    acmeData = QFile(":acme")
    if not acmeData.open(QIODevice.ReadOnly | QIODevice.Text):
        sys.exit(1)

    categories = []

    dataReader = CandlestickDataReader(acmeData)
    while not dataReader.atEnd():
        _set = dataReader.readCandlestickSet()
        if _set is not None:
            acmeSeries.append(_set)
            categories.append(
                QDateTime.fromMSecsSinceEpoch(int(_set.timestamp())).toString("dd")
            )

    chart = QChart()
    chart.addSeries(acmeSeries)
    chart.setTitle("Acme Ltd Historical Data (July 2015)")
    chart.setAnimationOptions(QChart.SeriesAnimations)

    chart.createDefaultAxes()

    axisX = chart.axes(Qt.Horizontal)[0]
    axisX.setCategories(categories)

    axisY = chart.axes(Qt.Vertical)[0]
    axisY.setMax(axisY.max() * 1.01)
    axisY.setMin(axisY.min() * 0.99)

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()

    sys.exit(a.exec_())


if __name__ == "__main__":
    main()
