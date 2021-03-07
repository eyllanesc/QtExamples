# -*- coding: utf-8 -*-
import threading

import shiboken2
from PySide2.QtCore import Property, QTimer, QObject, QSize, Signal, Slot
from PySide2.QtGui import QImage
from PySide2.QtMultimedia import (
    QAbstractVideoSurface,
    QVideoFrame,
    QVideoSurfaceFormat,
)

import cv2
import numpy as np

import qimage2ndarray

import mss

_sources = set()


class register_captuter(object):
    def __init__(self, name_of_source):
        self._name_of_source = name_of_source

    def __call__(self, cls):

        if BaseThreadCapturer not in cls.mro():
            raise TypeError(
                "Cannot register a class as a source: wrong type {}".format(cls)
            )

        Source = type(
            self._name_of_source,
            (BaseThreadSource,),
            {
                "__init__": lambda this, parent=None: BaseThreadSource.__init__(
                    this, cls, parent
                )
            },
        )

        _sources.add((Source, self._name_of_source))
        return cls


class BaseThreadCapturer(QObject):
    started = Signal()
    imageChanged = Signal(QImage)
    readFinished = Signal(np.ndarray)
    convertFinished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._timer = QTimer(singleShot=True, interval=0, timeout=self._handle_timeout)

        self.readFinished.connect(self.convert_cv_to_qimage)
        self.convertFinished.connect(self._timer.start)

        self._is_stopped = threading.Event()
        self._parameters = None

        self._thread = None

    @property
    def parameters(self):
        return self._parameters

    @Slot("QVariant")
    def start(self, parameters):
        self._is_stopped.clear()
        self._timer.start()
        self.started.emit()
        self._parameters = parameters

    @Slot()
    def stop(self):
        if self._timer.isActive():
            self._timer.stop()
        self._is_stopped.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join()
            self._thread = None

    def _handle_timeout(self):
        self._thread = threading.Thread(target=self._read_from_capture, daemon=True)
        self._thread.start()

    def _read_from_capture(self):
        if self._is_stopped.isSet():
            return

        ret, frame = self.read()
        if ret and shiboken2.isValid(self):
            self.readFinished.emit(frame.copy())

    @Slot(np.ndarray)
    def convert_cv_to_qimage(self, frame):
        result = self.convert(frame)
        qimage = qimage2ndarray.array2qimage(result)
        self.imageChanged.emit(qimage.copy())
        self.convertFinished.emit()

    def read(self):
        return True, np.ndarray()

    def convert(self, frame):
        return QImage()


class BaseThreadSource(QObject):
    surfaceChanged = Signal()
    sourceChanged = Signal()

    def __init__(self, KlassCapturer, parent=None):
        super().__init__(parent)
        self._surface = None
        self._format = QVideoSurfaceFormat()
        self._format_is_valid = False
        self._source = None

        self._capturer = KlassCapturer()
        self._capturer.imageChanged.connect(self.update_frame)

    @Property("QVariant", notify=sourceChanged)
    def source(self):
        return self._source

    @source.setter
    def source(self, s):
        if self._source == s:
            return
        self._source = s
        self.sourceChanged.emit()

    @Property(QAbstractVideoSurface, notify=surfaceChanged)
    def videoSurface(self):
        return self._surface

    @videoSurface.setter
    def videoSurface(self, surface):
        if self.videoSurface is surface:
            return
        if (
            self.videoSurface is not None
            and self.videoSurface is not surface
            and self.videoSurface.isActive()
        ):
            self.videoSurface.stop()
        self._surface = surface
        self.surfaceChanged.emit()

        if self.videoSurface is not None:
            self._format = self.videoSurface.nearestFormat(self._format)
            self.videoSurface.start(self._format)

    @Slot()
    def start(self):
        self._capturer.start(self.source)

    @Slot()
    def stop(self):
        self._capturer.stop()

    @Slot(QImage)
    def update_frame(self, qimage):
        if self.videoSurface is None or qimage.isNull():
            return
        if not self._format_is_valid:
            self._set_format(qimage.width(), qimage.height(), QVideoFrame.Format_RGB32)
            self._format_is_valid = True
        qimage.convertTo(
            QVideoFrame.imageFormatFromPixelFormat(QVideoFrame.Format_RGB32)
        )
        self.videoSurface.present(QVideoFrame(qimage))

    def _set_format(self, width, height, pixel_format):
        size = QSize(width, height)
        video_format = QVideoSurfaceFormat(size, pixel_format)
        self._format = video_format
        if self.videoSurface is not None:
            if self.videoSurface.isActive():
                self.videoSurface.stop()
            self._format = self.videoSurface.nearestFormat(self._format)
            self.videoSurface.start(self._format)


@register_captuter("CVSource")
class CVCapturer(BaseThreadCapturer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._video_capture = None

    @Slot("QVariant")
    def start(self, parameters):
        self.stop()
        if self._video_capture is not None:
            self._video_capture.release()
        self._video_capture = cv2.VideoCapture(parameters)
        if self._video_capture.isOpened():
            super().start(parameters)

    @Slot()
    def stop(self):
        if self._video_capture is not None:
            self._video_capture.release()
        self._video_capture = None
        super().stop()

    def read(self):
        if self._video_capture is not None:
            return self._video_capture.read()
        return False, None

    def convert(self, frame):
        if frame is None:
            return QImage()
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


@register_captuter("MSSSource")
class MSSCapturer(BaseThreadCapturer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._sct = mss.mss()

    def read(self):
        monitor = self._sct.monitors[self.parameters]
        return True, np.array(self._sct.grab(monitor))

    def convert(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
