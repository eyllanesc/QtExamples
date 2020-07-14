from functools import singledispatch

from Qt.QtCore import Slot
from Qt.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat
from Qt.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget

from audiodevicesbase_ui import Ui_AudioDevicesBase


@singledispatch
def toString(value) -> str:
    raise NotImplementedError


@toString.register
def _(value: QAudioFormat.SampleType) -> str:
    return {
        QAudioFormat.SignedInt: "SignedInt",
        QAudioFormat.UnSignedInt: "UnSignedInt",
        QAudioFormat.Float: "Float",
        QAudioFormat.Unknown: "Unknown",
    }.get(value, "Unknown")


@toString.register
def _(value: QAudioFormat.Endian) -> str:
    return {
        QAudioFormat.LittleEndian: "LittleEndian",
        QAudioFormat.BigEndian: "BigEndian",
    }.get(value, "Unknown")


class AudioDevicesBase(QMainWindow, Ui_AudioDevicesBase):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi(self)


class AudioTest(AudioDevicesBase):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.m_deviceInfo: QAudioDeviceInfo = QAudioDeviceInfo()
        self.m_settings: QAudioFormat = QAudioFormat()

        self.testButton.clicked.connect(self.test)
        self.modeBox.activated[int].connect(self.modeChanged)
        self.deviceBox.activated[int].connect(self.deviceChanged)
        self.sampleRateBox.activated[int].connect(self.sampleRateChanged)
        self.channelsBox.activated[int].connect(self.channelChanged)
        self.codecsBox.activated[int].connect(self.codecChanged)
        self.sampleSizesBox.activated[int].connect(self.sampleSizeChanged)
        self.sampleTypesBox.activated[int].connect(self.sampleTypeChanged)
        self.endianBox.activated[int].connect(self.endianChanged)
        self.populateTableButton.clicked.connect(self.populateTable)

        self.modeBox.setCurrentIndex(0)
        self.modeChanged(0)
        self.deviceBox.setCurrentIndex(0)
        self.deviceChanged(0)

    @Slot()
    def test(self) -> None:
        self.testResult.clear()
        if not self.m_deviceInfo.isNull():
            if self.m_deviceInfo.isFormatSupported(self.m_settings):
                self.testResult.setText(self.tr("Success"))
                self.nearestSampleRate.clear()
                self.nearestChannel.clear()
                self.nearestCodec.clear()
                self.nearestSampleSize.clear()
                self.nearestSampleType.clear()
                self.nearestEndian.clear()
            else:
                nearest = self.m_deviceInfo.nearestFormat(self.m_settings)
                self.testResult.setText(self.tr("Failed"))
                self.nearestSampleRate.setText(f"{nearest.sampleRate()}")
                self.nearestChannel.setText(f"{nearest.channelCount()}")
                self.nearestCodec.setText(nearest.codec())
                self.nearestSampleSize.setText(f"{nearest.sampleSize()}")
                self.nearestSampleType.setText(toString(nearest.sampleType()))
                self.nearestEndian.setText(toString(nearest.byteOrder()))
        else:
            self.testResult.setText(self.tr("No Device"))

    @Slot(int)
    def modeChanged(self, idx: int) -> None:
        self.testResult.clear()
        self.deviceBox.clear()
        mode = QAudio.AudioInput if idx == 0 else QAudio.AudioOutput
        for deviceInfo in QAudioDeviceInfo.availableDevices(mode):
            self.deviceBox.addItem(deviceInfo.deviceName(), deviceInfo)
        self.deviceBox.setCurrentIndex(0)
        self.deviceChanged(0)

    @Slot(int)
    def deviceChanged(self, idx: int) -> None:
        self.testResult.clear()

        if self.deviceBox.count() == 0:
            return

        self.m_deviceInfo = self.deviceBox.itemData(idx)

        self.sampleRateBox.clear()
        sample_rates = self.m_deviceInfo.supportedSampleRates()
        for sample_rate in sample_rates:
            self.sampleRateBox.addItem(f"{sample_rate}")
        if sample_rates:
            self.m_settings.setSampleRate(sample_rates[0])

        self.channelsBox.clear()
        channels = self.m_deviceInfo.supportedChannelCounts()
        for channel in channels:
            self.channelsBox.addItem(f"{channel}")
        if channels:
            self.m_settings.setChannelCount(channels[0])

        self.codecsBox.clear()
        codecs = self.m_deviceInfo.supportedCodecs()
        for codec in codecs:
            self.codecsBox.addItem(f"{codec}")
        if codecs:
            self.m_settings.setCodec(codecs[0])
        self.codecsBox.addItem("audio/test")

        self.sampleSizesBox.clear()
        sample_sizes = self.m_deviceInfo.supportedSampleSizes()
        for sample_size in sample_sizes:
            self.sampleSizesBox.addItem(f"{sample_size}")
        if sample_sizes:
            self.m_settings.setSampleSize(sample_sizes[0])

        self.sampleTypesBox.clear()
        sample_types = self.m_deviceInfo.supportedSampleTypes()
        for sample_type in sample_types:
            self.sampleTypesBox.addItem(toString(sample_type))
        if sample_types:
            self.m_settings.setSampleType(sample_types[0])

        self.endianBox.clear()
        endians = self.m_deviceInfo.supportedByteOrders()
        for endian in endians:
            self.endianBox.addItem(toString(endian))
        if endians:
            self.m_settings.setByteOrder(endians[0])

        self.allFormatsTable.clearContents()

    @Slot()
    def populateTable(self) -> None:
        row = 0
        format = QAudioFormat()
        for codec in self.m_deviceInfo.supportedCodecs():
            format.setCodec(codec)
            for sample_rate in self.m_deviceInfo.supportedSampleRates():
                format.setSampleRate(sample_rate)
                for channel_count in self.m_deviceInfo.supportedChannelCounts():
                    format.setChannelCount(channel_count)
                    for sample_type in self.m_deviceInfo.supportedSampleTypes():
                        format.setSampleType(sample_type)
                        for sample_size in self.m_deviceInfo.supportedSampleSizes():
                            format.setSampleType(sample_type)
                            for endian in self.m_deviceInfo.supportedByteOrders():
                                format.setByteOrder(endian)
                                self.allFormatsTable.setRowCount(row + 1)

                                codecItem = QTableWidgetItem(format.codec())
                                self.allFormatsTable.setItem(row, 0, codecItem)

                                sampleRateItem = QTableWidgetItem(
                                    f"{format.sampleRate()}"
                                )
                                self.allFormatsTable.setItem(row, 1, sampleRateItem)

                                channelsItem = QTableWidgetItem(
                                    f"{format.channelCount()}"
                                )
                                self.allFormatsTable.setItem(row, 2, channelsItem)

                                sampleTypeItem = QTableWidgetItem(
                                    toString(format.sampleType())
                                )
                                self.allFormatsTable.setItem(row, 3, sampleTypeItem)

                                sampleSizeItem = QTableWidgetItem(
                                    f"{format.sampleSize()}"
                                )
                                self.allFormatsTable.setItem(row, 4, sampleSizeItem)

                                byteOrderItem = QTableWidgetItem(
                                    toString(format.byteOrder())
                                )
                                self.allFormatsTable.setItem(row, 5, byteOrderItem)

                                row += 1

    @Slot(int)
    def sampleRateChanged(self, idx: int) -> None:
        try:
            rate = int(self.sampleRateBox.itemText(idx))
        except ValueError:
            rate = -1
        else:
            self.m_settings.setSampleRate(rate)

    @Slot(int)
    def channelChanged(self, idx: int) -> None:
        try:
            count = int(self.channelsBox.itemText(idx))
        except ValueError:
            count = -1
        else:
            self.m_settings.setChannelCount(count)

    @Slot(int)
    def codecChanged(self, idx: int) -> None:
        self.m_settings.setCodec(self.codecsBox.itemText(idx))

    @Slot(int)
    def sampleSizeChanged(self, idx: int) -> None:
        try:
            size = int(self.sampleSizesBox.itemText(idx))
        except ValueError:
            size = -1
        else:
            self.m_settings.setSampleSize(size)

    @Slot(int)
    def sampleTypeChanged(self, idx: int) -> None:
        try:
            sample_type = int(self.sampleTypesBox.itemText(idx))
        except ValueError:
            sample_type = -1
        else:
            if sample_type == QAudioFormat.SignedInt:
                self.m_settings.setSampleType(QAudioFormat.SignedInt)
            elif sample_type == QAudioFormat.UnSignedInt:
                self.m_settings.setSampleType(QAudioFormat.UnSignedInt)
            elif sample_type == QAudioFormat.Float:
                self.m_settings.setSampleType(QAudioFormat.Float)

    @Slot(int)
    def endianChanged(self, idx: int) -> None:
        try:
            byte_order = int(self.endianBox.itemText(idx))
        except ValueError:
            byte_order = -1
        else:
            if byte_order == QAudioFormat.LittleEndian:
                self.m_settings.setByteOrder(QAudioFormat.LittleEndian)
            elif byte_order == QAudioFormat.BigEndian:
                self.m_settings.setByteOrder(QAudioFormat.BigEndian)


def main() -> None:
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("Audio Device Test")

    audio = AudioTest()
    audio.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
