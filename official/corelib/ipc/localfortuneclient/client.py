from Qt.QtCore import QDataStream, Qt, QTimer, Slot
from Qt.QtGui import QGuiApplication
from Qt.QtNetwork import QLocalSocket
from Qt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)


class Client(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._in = QDataStream()
        self.blockSize = 0

        self.currentFortune = ""

        self.hostLineEdit = QLineEdit("fortune")
        self.getFortuneButton = QPushButton(self.tr("Get Fortune"))
        self.statusLabel = QLabel(
            self.tr(
                "This examples requires that you run the Local Fortune Server example as well."
            )
        )
        self.socket = QLocalSocket()

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        hostLabel = QLabel(self.tr("&Server name:"))
        hostLabel.setBuddy(self.hostLineEdit)

        self.statusLabel.setWordWrap(True)

        self.getFortuneButton.setDefault(True)
        quitButton = QPushButton(self.tr("Quit"))

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        self._in.setDevice(self.socket)
        self._in.setVersion(QDataStream.Qt_5_10)

        self.hostLineEdit.textChanged.connect(self.enableGetFortuneButton)

        self.getFortuneButton.clicked.connect(self.requestNewFortune)
        quitButton.clicked.connect(self.close)
        self.socket.readyRead.connect(self.readFortune)
        self.socket.errorOccurred.connect(self.displayError)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostLineEdit, 0, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 3, 0, 1, 2)

        self.setWindowTitle(QGuiApplication.applicationDisplayName())
        self.hostLineEdit.setFocus()

    @Slot()
    def requestNewFortune(self):
        self.getFortuneButton.setEnabled(False)
        self.blockSize = 0
        self.socket.abort()
        self.socket.connectToServer(self.hostLineEdit.text())

    @Slot()
    def readFortune(self):
        if self.blockSize == 0:
            # Relies on the fact that QDataStream serializes a quint32 into
            # sizeof(quint32) bytes
            if self.socket.bytesAvailable() < 4:  # (int)sizeof(quint32))
                return
            self.blockSize = self._in.readUInt32()

        if self.socket.bytesAvailable() < self.blockSize or self._in.atEnd():
            return

        nextFortune = ""
        nextFortune = self._in.readQString()

        if nextFortune == self.currentFortune:
            QTimer.singleShot(0, self.requestNewFortune)
            return

        currentFortune = nextFortune
        self.statusLabel.setText(currentFortune)
        self.getFortuneButton.setEnabled(True)

    @Slot(QLocalSocket.LocalSocketError)
    def displayError(self, socketError):
        if socketError == QLocalSocket.ServerNotFoundError:

            QMessageBox.information(
                self,
                self.tr("Local Fortune Client"),
                self.tr(
                    "The host was not found. Please make sure "
                    "that the server is running and that the "
                    "server name is correct."
                ),
            )
        elif socketError == QLocalSocket.ConnectionRefusedError:
            QMessageBox.information(
                self,
                self.tr("Local Fortune Client"),
                self.tr(
                    "The connection was refused by the peer. "
                    "Make sure the fortune server is running, "
                    "and check that the server name is correct."
                ),
            )
        elif socketError == QLocalSocket.PeerClosedError:
            return
        else:
            QMessageBox.information(
                self,
                self.tr("Local Fortune Client"),
                self.tr(
                    "The following error occurred: %s." % (self.socket.errorString())
                ),
            )

        self.getFortuneButton.setEnabled(True)

    @Slot()
    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(bool(self.hostLineEdit.ext()))
