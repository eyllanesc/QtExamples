# -*- coding: utf-8 -*-
from PySide2.QtCore import QPointF, QRectF, Signal
from PySide2.QtMultimedia import (
    QAbstractVideoBuffer,
    QAbstractVideoFilter,
    QVideoFilterRunnable,
    QVideoFrame,
)

import cv2
import numpy as np
import qimage2ndarray

from pyzbar.pyzbar import decode as pyzbar_decode

_filters = set()


class BaseFilterRunnable(QVideoFilterRunnable):
    def __init__(self, video_filter):
        super().__init__()
        self._video_filter = video_filter

    @property
    def video_filter(self):
        return self._video_filter


class register_runnable_filter(object):
    def __init__(self, *, name_of_filter, klass_filter=None):
        if klass_filter is not None and QAbstractVideoFilter not in klass_filter.mro():
            raise TypeError(
                "Cannot register a class as a Filter: wrong type {}".format(
                    klass_filter
                )
            )
        self._klass_filter = klass_filter
        self._name_of_filter = name_of_filter

    def __call__(self, function):
        def run(this, _input, surfaceFormat, flags):
            _input.map(QAbstractVideoBuffer.ReadOnly)
            qimage = _input.image()
            _input.unmap()

            frame_in = qimage2ndarray.rgb_view(qimage)
            frame_out = function(this.video_filter, frame_in)

            if frame_out is not None:
                return QVideoFrame(qimage2ndarray.array2qimage(frame_out))
            return _input

        Runnable = type(
            self._name_of_filter + "Runnable",
            (BaseFilterRunnable,),
            {
                "run": run,
            },
        )

        Filter = type(
            self._name_of_filter,
            (self._klass_filter or QAbstractVideoFilter,),
            {"createFilterRunnable": lambda this: Runnable(this)},
        )
        _filters.add((Filter, self._name_of_filter))

        return function


@register_runnable_filter(name_of_filter="MaxRGBFilter")
def max_rgn(video_filter, frame):
    frame_max = max_rgb_filter(frame)
    return frame_max


def max_rgb_filter(image):
    # split the image into its BGR components
    (R, G, B) = cv2.split(image)

    # find the maximum pixel intensity values for each
    # (x, y)-coordinate,, then set all pixel values less
    # than M to zero
    M = np.maximum(np.maximum(R, G), B)
    R[R < M] = 0
    G[G < M] = 0
    B[B < M] = 0

    # merge the channels back together and return the image
    return cv2.merge([R, G, B])


class ObjectsFilter(QAbstractVideoFilter):
    objectsDetected = Signal("QVariantList")

    face_cascade_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )


@register_runnable_filter(name_of_filter="ObjectsFilter", klass_filter=ObjectsFilter)
def run_face_classifier(video_filter, frame):
    width, height = 100, 100
    frame = cv2.resize(frame, (width, height))
    width, height, _ = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = video_filter.face_cascade_classifier.detectMultiScale(
        gray, 1.1, 3, cv2.CASCADE_DO_ROUGH_SEARCH | cv2.CASCADE_FIND_BIGGEST_OBJECT
    )
    rects = []
    for (x, y, w, h) in faces:
        rect = QRectF(
            x * 1.0 / width,
            y * 1.0 / height,
            w * 1.0 / width,
            h * 1.0 / height,
        )
        rects.append(rect)
    video_filter.objectsDetected.emit(rects)


class BarcodeFilter(QAbstractVideoFilter):
    barcodesDetected = Signal("QVariantList")


@register_runnable_filter(name_of_filter="BarcodeFilter", klass_filter=BarcodeFilter)
def run_barcode(video_filter, frame):
    height, width, _ = frame.shape
    """width, height = 100, 100
    frame = cv2.resize(frame, (width, height))"""

    barcodes = pyzbar_decode(frame)

    barcodes_detected = []
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        rect = QRectF(
            x * 1.0 / width,
            y * 1.0 / height,
            w * 1.0 / width,
            h * 1.0 / height,
        )
        points = []
        for point in barcode.polygon:
            p = QPointF(point.x * 1.0 / width, point.y * 1.0 / height)
            points.append(p)

        barcodes_detected.append(
            {
                "data": barcode.data.decode("utf-8"),
                "type": barcode.type,
                "rect": rect,
                "polygon": points,
            }
        )
        video_filter.barcodesDetected.emit(barcodes_detected)


@register_runnable_filter(name_of_filter="StylizationFilter")
def stylization(video_filter, frame):
    width, height = 400, 400
    frame = cv2.resize(frame, (width, height))

    dst = cv2.stylization(frame, sigma_s=60, sigma_r=0.07)

    return dst
