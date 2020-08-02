from functools import cached_property
import random

from PyQt5.QtCore import Qt, QUrl, QPointF, QRectF, QVariantAnimation
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QMainWindow,
)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem


class VideoGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self._aspectRatioMode = Qt.KeepAspectRatio
        scene = QGraphicsScene(self)
        self.setScene(scene)
        self.scene().addItem(self.videoItem)
        self.player.setVideoOutput(self.videoItem)

        self.player.mediaStatusChanged.connect(self._fix_size)

        self.videoItem.nativeSizeChanged.connect(self._handle_native_size_changed)

    @cached_property
    def player(self):
        return QMediaPlayer(self, QMediaPlayer.VideoSurface)

    @cached_property
    def videoItem(self):
        return QGraphicsVideoItem()

    @property
    def aspectRatioMode(self):
        return self._aspectRatioMode

    @aspectRatioMode.setter
    def aspectRatioMode(self, mode):
        if self._aspectRatioMode != mode:
            self._aspectRatioMode = mode
            self.fitInView(self.videoItem, self.aspectRatioMode)

    def _handle_native_size_changed(self, size):
        self.scene().setSceneRect(QRectF(QPointF(0, 0), size))

    def resizeEvent(self, event):
        self._fix_size()
        super().resizeEvent(event)

    def _fix_size(self):
        self.fitInView(
            QRectF(QPointF(0, 0), self.videoItem.nativeSize()), self.aspectRatioMode
        )


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = VideoGraphicsView()
        self.setCentralWidget(self.view)

        self.view.videoItem.nativeSizeChanged.connect(self.handle_native_size_changed)

        url = QUrl(
            "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4"
        )
        self.view.player.setMedia(QMediaContent(url))
        self.view.player.play()

        self.resize(640, 480)

        self.text_item = QGraphicsTextItem(self.view.videoItem)
        self.text_item.setHtml(
            """<div style="color: #41CD52; font-weight: bold; font-size: 20px;">Qt is awesome</div>"""
        )
        self.text_item.hide()

        self.animation = QVariantAnimation()
        self.animation.setDuration(1000)
        self.animation.setStartValue(QPointF(0.0, 0.0))
        self.animation.setEndValue(QPointF(0.0, 0.0))
        self.animation.valueChanged.connect(self.text_item.setPos)
        self.animation.finished.connect(self.start_of_start_animation)

    def handle_native_size_changed(self):
        self.start_of_start_animation()

    def start_of_start_animation(self):
        w = self.view.videoItem.size().width() - self.text_item.boundingRect().width()
        h = self.view.videoItem.size().height() - self.text_item.boundingRect().height()
        end_pos_x = random.uniform(0, w)
        end_pos_y = random.uniform(0, h)
        self.animation.setStartValue(self.animation.endValue())
        self.animation.setEndValue(QPointF(end_pos_x, end_pos_y))
        self.text_item.show()
        self.animation.start()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
