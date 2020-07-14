from Qt.QtChart import QBoxPlotSeries, QChart, QChartView
from Qt.QtCore import QFile, QIODevice, Qt
from Qt.QtGui import QPainter
from Qt.QtWidgets import QApplication, QMainWindow

import boxplotdata_rc  # noqa: F401
from boxdatareader import BoxDataReader


def main():
    import sys

    app = QApplication(sys.argv)

    acmeSeries = QBoxPlotSeries()
    acmeSeries.setName("Acme Ltd")

    boxWhiskSeries = QBoxPlotSeries()
    boxWhiskSeries.setName("BoxWhisk Inc")

    acmeData = QFile(":acme")
    if not acmeData.open(QIODevice.ReadOnly | QIODevice.Text):
        sys.exit(1)

    dataReader = BoxDataReader(acmeData)
    while not dataReader.atEnd():
        _set = dataReader.readBox()
        if _set is not None:
            acmeSeries.append(_set)

    boxwhiskData = QFile(":boxwhisk")
    if not boxwhiskData.open(QIODevice.ReadOnly | QIODevice.Text):
        sys.exit(1)

    dataReader.readFile(boxwhiskData)
    while not dataReader.atEnd():
        _set = dataReader.readBox()
        if _set is not None:
            boxWhiskSeries.append(_set)

    chart = QChart()
    chart.addSeries(acmeSeries)
    chart.addSeries(boxWhiskSeries)
    chart.setTitle("Acme Ltd and BoxWhisk Inc share deviation in 2012")
    chart.setAnimationOptions(QChart.SeriesAnimations)

    chart.createDefaultAxes()
    chart.axes(Qt.Vertical)[0].setMin(15.0)
    chart.axes(Qt.Vertical)[0].setMax(34.0)

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
