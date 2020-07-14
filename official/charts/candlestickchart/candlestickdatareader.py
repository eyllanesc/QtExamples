from Qt.QtChart import QCandlestickSet
from Qt.QtCore import QTextStream


class CandlestickDataReader(QTextStream):
    def __init__(self, device):
        super().__init__(device)

    def readFile(self, device):
        self.setDevice(device)

    def readCandlestickSet(self):
        line = self.readLine()
        if line.startswith("#") or not line:
            return

        strList = line.split(" ")
        if len(strList) != 5:
            return

        timestamp, _open, high, low, close = [float(v) for v in strList]

        candlestickSet = QCandlestickSet(timestamp)
        candlestickSet.setOpen(_open)
        candlestickSet.setHigh(high)
        candlestickSet.setLow(low)
        candlestickSet.setClose(close)

        return candlestickSet
