# -*- coding: utf-8 -*-
charts_class = [
    "QAreaSeries",
    "QBarCategoryAxis",
    "QBarSeries",
    "QBarSet",
    "QChart",
    "QChartView",
    "QLineSeries",
    "QValueAxis",
    "QXYSeries",
    "QBoxPlotSeries",
    "QBoxSet",
    "QSplineSeries",
    "QCandlestickSeries",
    "QCandlestickSet",
]


def update_members(members):
    members["QtCore"] += [
        "QSharedMemory",
        "QCommandLineParser",
        "QMimeDatabase",
        "QStandardPaths",
    ]
    members["QtSerialPort"] = ["QSerialPortInfo"]
    members["QtQml"] = [
        "QQmlEngine",
        "QQmlApplicationEngine",
        "qmlRegisterType",
        "QQmlContext",
    ]
    members["QtQuick"] = ["QQuickItem", "QQuickView", "QQuickWindow"]
    members["QtGui"] += ["QGuiApplication", "QBackingStore", "QExposeEvent", "QWindow"]
    members["QtChart"] = list(charts_class)
    members["QtWebEngineCore"] = [
        "QWebEngineCookieStore",
        "QWebEngineUrlRequestJob",
        "QWebEngineUrlScheme",
        "QWebEngineUrlSchemeHandler",
    ]
    members["QtWebEngineWidgets"] = [
        "QWebEnginePage",
        "QWebEngineView",
        "QWebEngineProfile",
    ]
    members["QtWebChannel"] = ["QWebChannel"]
    members["QtWebSockets"] = ["QWebSocketServer"]
    members["QtNetwork"] += [
        "QSslConfiguration",
        "QSslCertificate",
        "QSslKey",
        "QSslSocket",
    ]


def _PySide2_chart_class(cls_name):
    from PySide2.QtCharts import QtCharts

    return getattr(QtCharts, cls_name)


def update_misplaced_members(members):
    for cls_name in charts_class:
        n = ".".join(["QtChart", cls_name])
        members["PySide2"][n] = [n, _PySide2_chart_class(cls_name)]
