from qtpy.QtCore import QPointF, QRect, QTimer, Qt
from qtpy.QtGui import (
    QBrush,
    QGuiApplication,
    QLinearGradient,
    QMatrix4x4,
    QPainter,
    QPainterPath,
    QRasterWindow,
    QVector3D,
)


def painterPathForTriangle():
    bottomLeft = QPointF(-1.0, -1.0)
    top = QPointF(0.0, 1.0)
    bottomRight = QPointF(1.0, -1.0)

    path = QPainterPath(bottomLeft)
    path.lineTo(top)
    path.lineTo(bottomRight)
    path.closeSubpath()
    return path


class PaintedWindow(QRasterWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_window_matrix = QMatrix4x4()
        self.m_projection = QMatrix4x4()
        self.m_view = QMatrix4x4()
        self.m_model = QMatrix4x4()
        self.m_brush = QBrush()
        self.m_timer = QTimer()

        self.m_view.lookAt(QVector3D(3, 1, 1), QVector3D(0, 0, 0), QVector3D(0, 1, 0))
        self.m_timer.setInterval(16)
        self.m_timer.timeout.connect(self.update)
        self.m_timer.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(QRect(0, 0, self.width(), self.height()), Qt.gray)

        p.setWorldTransform(self.m_window_matrix.toTransform())

        mvp = QMatrix4x4(self.m_projection * self.m_view * self.m_model)
        p.setTransform(mvp.toTransform(), True)

        p.fillPath(painterPathForTriangle(), self.m_brush)

        self.m_model.rotate(1, 0, 1, 0)

    def resizeEvent(self, event):
        if self.width() <= 0:
            return
        self.m_window_matrix = QMatrix4x4()
        self.m_window_matrix.translate(self.width() / 2.0, self.height() / 2.0)
        self.m_window_matrix.scale(self.width() / 2.0, -self.height() / 2.0)

        self.m_projection.setToIdentity()
        self.m_projection.perspective(
            45.0, self.width() * 1.0 / self.height(), 0.1, 100.0
        )

        gradient = QLinearGradient(QPointF(-1, -1), QPointF(1, 1))
        gradient.setColorAt(0, Qt.red)
        gradient.setColorAt(1, Qt.green)

        self.m_brush = QBrush(gradient)


def main():
    import sys

    app = QGuiApplication(sys.argv)

    w = PaintedWindow()
    w.create()
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
