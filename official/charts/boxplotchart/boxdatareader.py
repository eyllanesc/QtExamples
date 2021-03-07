# -*- coding: utf-8 -*-
from Qt.QtChart import QBoxSet
from Qt.QtCore import QTextStream


class BoxDataReader(QTextStream):
    def __init__(self, device):
        super().__init__(device)

        self.sortedList = []

    def readFile(self, device):
        super().setDevice(device)

    def readBox(self):
        line = self.readLine()

        if line.startswith("#"):
            return

        strList = line.split(" ")

        self.sortedList = []

        for e in strList[1:]:
            self.sortedList.append(float(e))

        self.sortedList.sort()

        count = len(self.sortedList)
        box = QBoxSet(strList[0])
        box.setValue(QBoxSet.LowerExtreme, self.sortedList[0])
        box.setValue(QBoxSet.UpperExtreme, self.sortedList[-1])
        box.setValue(QBoxSet.Median, self.findMedian(0, count))
        box.setValue(QBoxSet.LowerQuartile, self.findMedian(0, count // 2))
        box.setValue(
            QBoxSet.UpperQuartile, self.findMedian(count // 2 + (count % 2), count)
        )

        return box

    def findMedian(self, begin, end):
        count = end - begin
        if count % 2:
            return self.sortedList[count // 2 + begin]
        else:
            right = self.sortedList[count // 2 + begin]
            left = self.sortedList[count // 2 - 1 + begin]
            return (right + left) / 2.0
