from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.history_model = QtGui.QStandardItemModel(self)
        self.history_completer = QtWidgets.QCompleter(self)
        self.history_completer.setModel(self.history_model)

        self.pipeline_le = QtWidgets.QLineEdit()
        self.pipeline_le.setCompleter(self.history_completer)
        self.play_btn = QtWidgets.QPushButton(self.tr("&Play"))

        for text in (
            ('gst-pipeline: videotestsrc ! xvimagesink name="qtvideosink"'),
            (
                'gst-pipeline: v4l2src device="/dev/video0" ! video/x-raw,width=640,height=480 ! xvimagesink name="qtvideosink"'  # noqa: E501
            ),
            ('gst-pipeline: ximagesrc ! videoconvert ! xvimagesink name="qtvideosink"'),
        ):
            it = QtGui.QStandardItem(text)
            self.history_model.appendRow(it)

        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer(
            self, QtMultimedia.QMediaPlayer.VideoSurface
        )
        self.player.error.connect(self.on_error)
        self.player.setVideoOutput(self.video_widget)

        self.play_btn.clicked.connect(self.on_clicked)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        grid_layout = QtWidgets.QGridLayout(central_widget)
        grid_layout.addWidget(QtWidgets.QLabel(self.tr("<b>Url:</b>")), 0, 0)
        grid_layout.addWidget(self.pipeline_le, 0, 1)
        grid_layout.addWidget(self.play_btn, 0, 2)
        grid_layout.addWidget(self.video_widget, 1, 0, 1, 3)

        self.resize(640, 480)

    @QtCore.pyqtSlot()
    def on_clicked(self):
        text = self.pipeline_le.text()
        if not text:
            return
        if not self.history_model.findItems(text):
            it = QtGui.QStandardItem(text)
            self.history_model.appendRow(it)
        url = QtCore.QUrl(text)
        self.player.setMedia(QtMultimedia.QMediaContent(url))
        self.player.play()

    @QtCore.pyqtSlot(QtMultimedia.QMediaPlayer.Error)
    def on_error(self, error):
        print(f"error:  {error}")
        if error != QtMultimedia.QMediaPlayer.NoError:
            self.statusBar().showMessage(f"error: {self.player.errorString()}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
