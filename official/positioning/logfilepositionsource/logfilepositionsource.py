from PyQt5.QtCore import Qt, QDateTime, QFile, QIODevice, QTimer
from PyQt5.QtPositioning import QGeoCoordinate, QGeoPositionInfo, QGeoPositionInfoSource


class LogFilePositionSource(QGeoPositionInfoSource):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lastPosition = QGeoPositionInfo()

        self.logFile = QFile(self)
        self.timer = QTimer(self)

        self.timer.timeout.connect(self.readNextPosition)

        self.logFile.setFileName(":/simplelog.txt")
        if not self.logFile.open(QIODevice.ReadOnly):
            print("Error: cannot open source file", self.logFile.fileName())

    def lastKnownPosition(self, fromSatellitePositioningMethodsOnly=False):
        return self.lastPosition

    def supportedPositioningMethods(self):
        return QGeoPositionInfoSource.AllPositioningMethods

    def minimumUpdateInterval(self):
        return 500

    def error(self):
        return QGeoPositionInfoSource.NoError

    def startUpdates(self):
        interval = self.updateInterval()
        if interval < self.minimumUpdateInterval():
            interval = self.minimumUpdateInterval()
        self.timer.start(interval)

    def stopUpdates(self):
        self.timer.stop()

    def requestUpdate(self, timeout=5000):
        # For simplicity, ignore timeout - assume that if data is not available
        # now, no data will be added to the file later
        if self.logFile.canReadLine():
            self.readNextPosition()
        else:
            self.updateTimeout.emit()

    def readNextPosition(self):
        line = self.logFile.readLine().trimmed()
        if not line.isEmpty():
            data = line.split(" ")
            latitude = 0
            longitude = 0
            hasLatitude = False
            hasLongitude = False
            timestamp = QDateTime.fromString(data[0].data().decode(), Qt.ISODate)
            latitude, hasLatitude = data[1].toDouble()
            longitude, hasLongitude = data[2].toDouble()
            if hasLatitude and hasLongitude and timestamp.isValid():
                coordinate = QGeoCoordinate(latitude, longitude)
                info = QGeoPositionInfo(coordinate, timestamp)
                if info.isValid():
                    self.lastPosition = info
                    self.positionUpdated.emit(info)
