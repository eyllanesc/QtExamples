# -*- coding: utf-8 -*-
from Qt.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QXYSeries
from Qt.QtCore import QIODevice, QObject, QPointF, Qt
from Qt.QtMultimedia import QAudioDeviceInfo, QAudioFormat, QAudioInput
from Qt.QtWidgets import QApplication, QMessageBox, QVBoxLayout, QWidget


class XYSeriesIODevice(QIODevice):
    sampleCount = 2000

    def __init__(self, series: QXYSeries, parent: QObject = None):
        super().__init__(parent)
        self.m_series = series
        self.m_buffer = []

    def readData(self, data, max_size):
        return -1

    def writeData(self, data):
        max_size = len(data)
        resolution = 4

        if not self.m_buffer:
            for i in range(XYSeriesIODevice.sampleCount):
                self.m_buffer.append(QPointF(i, 0))

        start = 0
        available_samples = int(max_size) // resolution

        if available_samples < XYSeriesIODevice.sampleCount:
            start = XYSeriesIODevice.sampleCount - available_samples
            for s in range(0, start):
                self.m_buffer[s].setY(self.m_buffer[s + available_samples].y())

        pos = 0
        for s in range(start, XYSeriesIODevice.sampleCount):
            y = (1.0 * (data[pos] - 128)) / 128.0
            self.m_buffer[s].setY(y)
            pos += resolution
        self.m_series.replace(self.m_buffer)
        return (XYSeriesIODevice.sampleCount - start) * resolution


class Widget(QWidget):
    def __init__(self, device_info: QAudioDeviceInfo, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.m_chart = QChart()
        self.m_series = QLineSeries()

        chart_view = QChartView(self.m_chart)
        chart_view.setMinimumSize(800, 600)
        self.m_chart.addSeries(self.m_series)
        axisX = QValueAxis()
        axisX.setRange(0, XYSeriesIODevice.sampleCount)
        axisX.setLabelFormat("%g")
        axisX.setTitleText("Samples")
        axisY = QValueAxis()
        axisY.setRange(-1, 1)
        axisY.setTitleText("Audio level")
        self.m_chart.addAxis(axisX, Qt.AlignBottom)
        self.m_series.attachAxis(axisX)
        self.m_chart.addAxis(axisY, Qt.AlignLeft)
        self.m_series.attachAxis(axisY)
        self.m_chart.legend().hide()
        self.m_chart.setTitle(f"Data from the microphone ({device_info.deviceName()})")

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(chart_view)

        formatAudio = QAudioFormat()
        formatAudio.setSampleRate(8000)
        formatAudio.setChannelCount(1)
        formatAudio.setSampleSize(8)
        formatAudio.setCodec("audio/pcm")
        formatAudio.setByteOrder(QAudioFormat.LittleEndian)
        formatAudio.setSampleType(QAudioFormat.UnSignedInt)

        self.m_audioInput = QAudioInput(device_info, formatAudio, self)

        self.m_device = XYSeriesIODevice(self.m_series, self)
        self.m_device.open(QIODevice.WriteOnly)

        self.m_audioInput.start(self.m_device)


def main():
    import sys

    app = QApplication(sys.argv)

    input_device = QAudioDeviceInfo.defaultInputDevice()
    if input_device.isNull():
        QMessageBox.warning(None, "audio", "There is no audio input device available.")
        sys.exit(-1)

    w = Widget(input_device)
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
