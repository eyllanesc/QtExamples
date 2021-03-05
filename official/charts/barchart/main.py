from Qt.QtChart import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QValueAxis,
)
from Qt.QtCore import Qt
from Qt.QtGui import QPainter
from Qt.QtWidgets import QApplication, QMainWindow


def main():
    import sys

    app = QApplication(sys.argv)

    set0 = QBarSet("Jane")
    set1 = QBarSet("John")
    set2 = QBarSet("Axel")
    set3 = QBarSet("Mary")
    set4 = QBarSet("Samantha")

    set0 << 1 << 2 << 3 << 4 << 5 << 6
    set1 << 5 << 0 << 0 << 4 << 0 << 7
    set2 << 3 << 5 << 8 << 13 << 8 << 5
    set3 << 5 << 6 << 7 << 3 << 4 << 5
    set4 << 9 << 7 << 5 << 3 << 1 << 2

    series = QBarSeries()
    series.append(set0)
    series.append(set1)
    series.append(set2)
    series.append(set3)
    series.append(set4)

    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Simple barchart example")
    chart.setAnimationOptions(QChart.SeriesAnimations)

    categories = ("Jan", "Feb", "Mar", "Apr", "May", "Jun")
    axisX = QBarCategoryAxis()
    axisX.append(categories)
    chart.addAxis(axisX, Qt.AlignBottom)
    series.attachAxis(axisX)

    axisY = QValueAxis()
    axisY.setRange(0, 15)
    chart.addAxis(axisY, Qt.AlignLeft)
    series.attachAxis(axisY)

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(420, 300)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
