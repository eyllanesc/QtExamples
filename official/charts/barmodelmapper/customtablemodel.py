# -*- coding: utf-8 -*-
import random
from collections import defaultdict

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui import QColor


class CustomTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_data = []
        self.m_mapping = defaultdict(list)

        self.m_columnCount = 6
        self.m_rowCount = 12

        for i in range(self.m_rowCount):
            dataVec = []
            for k in range(self.m_columnCount):
                if k % 2 == 0:
                    dataVec.append(i * 50 + random.randint(0, 20))
                else:
                    dataVec.append(random.randint(0, 100))
            self.m_data.append(dataVec)

    def rowCount(self, parent=QModelIndex()):
        return len(self.m_data)

    def columnCount(self, paren=QModelIndex()):
        return self.m_columnCount

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return "201%d" % section
        else:
            return "%d" % (section + 1)

    def data(self, index, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self.m_data[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            for key, rect in self.m_mapping.items():
                if rect.contains(index.column(), index.row()):
                    return QColor(key)
            return QColor(Qt.white)

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            self.m_data[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable

    def addMapping(self, color, area):
        self.m_mapping[color] = area
