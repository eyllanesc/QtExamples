import sys

from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork

gsuggestUrl = "http://google.com/complete/search?output=toolbar&q=%s"
gsearchUrl = "http://www.google.com/search?q=%s"


class GSuggestCompletion(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.editor = parent

        self.popup = QtWidgets.QTreeWidget()
        self.popup.setWindowFlags(QtCore.Qt.Popup)
        self.popup.setFocusPolicy(QtCore.Qt.NoFocus)
        self.popup.setFocusProxy(parent)
        self.popup.setMouseTracking(True)

        self.popup.setColumnCount(1)
        self.popup.setUniformRowHeights(True)
        self.popup.setRootIsDecorated(False)
        self.popup.setEditTriggers(QtWidgets.QTreeWidget.NoEditTriggers)
        self.popup.setSelectionBehavior(QtWidgets.QTreeWidget.SelectRows)
        self.popup.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.popup.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.popup.header().hide()

        self.popup.installEventFilter(self)

        self.popup.itemClicked.connect(self.doneCompletion)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.autoSuggest)
        self.editor.textEdited.connect(self.timer.start)

        self.networkManager = QtNetwork.QNetworkAccessManager()
        self.networkManager.finished.connect(self.handleNetworkData)

    def eventFilter(self, obj, event):
        if obj is not self.popup:
            return False

        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.popup.hide()
            self.editor.setFocus()
            return True

        if event.type() == QtCore.QEvent.KeyPress:
            consumed = False
            key = event.key()

            if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
                self.doneCompletion()
                consumed = True

            if key == QtCore.Qt.Key_Escape:
                self.editor.setFocus()
                self.popup.hide()
                consumed = True

            if key not in (
                QtCore.Qt.Key_Up,
                QtCore.Qt.Key_Down,
                QtCore.Qt.Key_Home,
                QtCore.Qt.Key_End,
                QtCore.Qt.Key_PageUp,
                QtCore.Qt.Key_PageDown,
            ):
                self.editor.setFocus()
                self.editor.event(event)
                self.popup.hide()
            return consumed
        return False

    def showCompletion(self, choices):
        if not choices:
            return
        pal = self.editor.palette()
        color = pal.color(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText)

        self.popup.setUpdatesEnabled(False)
        self.popup.clear()

        for choice in choices:
            item = QtWidgets.QTreeWidgetItem(self.popup)
            item.setText(0, choice)
            item.setBackground(0, color)

        self.popup.setCurrentItem(self.popup.topLevelItem(0))
        self.popup.resizeColumnToContents(0)
        self.popup.setUpdatesEnabled(True)

        self.popup.move(self.editor.mapToGlobal(QtCore.QPoint(0, self.editor.height())))
        self.popup.setFocus()
        self.popup.show()

    @QtCore.pyqtSlot()
    def doneCompletion(self):
        self.timer.stop()
        self.popup.hide()
        self.editor.setFocus()
        item = self.popup.currentItem()
        if item:
            self.editor.setText(item.text(0))
            self.editor.returnPressed.emit()

    @QtCore.pyqtSlot()
    def preventSuggest(self):
        self.timer.stop()

    @QtCore.pyqtSlot()
    def autoSuggest(self):
        text = self.editor.text()
        url = gsuggestUrl % (text,)
        self.networkManager.get(QtNetwork.QNetworkRequest(QtCore.QUrl(url)))

    @QtCore.pyqtSlot("QNetworkReply*")
    def handleNetworkData(self, networkReply):
        url = networkReply.url()
        if networkReply.error() == QtNetwork.QNetworkReply.NoError:
            choices = []
            response = networkReply.readAll()
            xml = QtCore.QXmlStreamReader(response)
            while not xml.atEnd():
                xml.readNext()
                if xml.tokenType() == QtCore.QXmlStreamReader.StartElement:
                    if xml.name() == "suggestion":
                        ref = xml.attributes().value("data")
                        choices.append(ref)
            self.showCompletion(choices)
        networkReply.deleteLater()


class SearchBox(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.completer = GSuggestCompletion(self)

        self.returnPressed.connect(self.doSearch)

        self.setWindowTitle(self.tr("Search with Google"))

        self.adjustSize()
        self.resize(400, self.height())
        self.setFocus()

    @QtCore.pyqtSlot()
    def doSearch(self):
        self.completer.preventSuggest()
        url = gsearchUrl % (self.text(),)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))


def main():
    app = QtWidgets.QApplication(sys.argv)
    searchEdit = SearchBox()
    searchEdit.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
