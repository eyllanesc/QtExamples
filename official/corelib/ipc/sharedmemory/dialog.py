from Qt.QtCore import QBuffer, QDataStream, QSharedMemory, Slot
from Qt.QtGui import QImage, QPixmap
from Qt.QtWidgets import QDialog, QFileDialog, QWidget

from dialog_ui import Ui_Dialog


class Dialog(QDialog):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.sharedMemory = QSharedMemory("QSharedMemoryExample")

        self.ui.loadFromFileButton.clicked.connect(self.loadFromFile)
        self.ui.loadFromSharedMemoryButton.clicked.connect(self.loadFromMemory)
        self.setWindowTitle(self.tr("SharedMemory Example"))

    @Slot()
    def loadFromFile(self):
        if self.sharedMemory.isAttached():
            self.detach()

        self.ui.label.setText(self.tr("Select an image file"))

        fileName, _ = QFileDialog.getOpenFileName(
            None, "", "", self.tr("Images (*.png *.xpm *.jpg)")
        )

        image = QImage()
        if not image.load(fileName):
            self.ui.label.setText(
                self.tr("Selected file is not an image, please select another.")
            )
            return
        self.ui.label.setPixmap(QPixmap.fromImage(image))

        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        out = QDataStream(buffer)
        out << image
        size = buffer.size()

        if not self.sharedMemory.create(size):
            self.ui.label.setText(self.tr("Unable to create shared memory segment."))
            return

        self.sharedMemory.lock()
        size = min(self.sharedMemory.size(), size)
        self.sharedMemory.data()[:size] = buffer.data()[:size]
        self.sharedMemory.unlock()

    @Slot()
    def loadFromMemory(self):
        if not self.sharedMemory.attach():
            self.ui.label.setText(
                self.tr(
                    "Unable to attach to shared memory segment.\n"
                    "Load an image first."
                )
            )
            return

        buffer = QBuffer()
        _in = QDataStream(buffer)
        image = QImage()

        self.sharedMemory.lock()
        buffer.setData(self.sharedMemory.data())
        buffer.open(QBuffer.ReadOnly)
        _in >> image
        self.sharedMemory.unlock()

        self.sharedMemory.detach()
        self.ui.label.setPixmap(QPixmap.fromImage(image))

    def detach(self):
        if not self.sharedMemory.detach():
            self.ui.label.setText(self.tr("Unable to detach from shared memory."))
