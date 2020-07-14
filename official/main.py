import os
import sys

from Qt.QtCore import QObject, QProcess, QProcessEnvironment, Qt, Signal, Slot
from Qt.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QSplitter, QTreeView

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class Launcher(QObject):
    standard_output_signal = Signal(str)
    standard_error_signal = Signal(str)

    def start(self, script: str, binding: str) -> None:
        process = QProcess(self)
        process.readyReadStandardError.connect(self._handle_standard_error)
        process.readyReadStandardOutput.connect(self._handle_standard_output)
        process.stateChanged.connect(print)

        env = QProcessEnvironment.systemEnvironment()
        env.insert("QT_DEBUG_PLUGINS", "1")
        env.insert("PYTHONPATH", os.path.join(CURRENT_DIR, "vendor"))
        env.insert("QT_PREFERRED_BINDING", binding)
        process.setProcessEnvironment(env)

        process.start(sys.executable, [script])

    @Slot()
    def _handle_standard_error(self):
        process: QProcess = self.sender()
        err = process.readAllStandardError().data().decode()
        self.standard_error_signal.emit(err)

    @Slot()
    def _handle_standard_output(self):
        process: QProcess = self.sender()
        out = process.readAllStandardOutput().data().decode()
        self.standard_output_signal.emit(out)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.launcher = Launcher()
        self.launcher.standard_output_signal.connect(self.handle_stdout)
        self.launcher.standard_error_signal.connect(self.handle_stderr)

        self.log_edit = QPlainTextEdit(readOnly=True)
        self.launcher_view = QTreeView()

        splitter = QSplitter(orientation=Qt.Vertical)
        splitter.addWidget(self.launcher_view)
        splitter.addWidget(self.log_edit)
        splitter.setSizes([10, 1])
        self.setCentralWidget(splitter)
        self.resize(640, 480)

        filename = os.path.join(CURRENT_DIR, "quickcontrols2/gallery/main.py")

        self.start(filename, "PySide2")

    def start(self, path_of_script, binding):
        self.log_edit.appendPlainText(f"Start: {path_of_script}")
        self.launcher.start(path_of_script, binding)

    def handle_stdout(self, msg):
        self.log_edit.appendPlainText(msg)

    def handle_stderr(self, msg):
        self.log_edit.appendPlainText(msg)


def main():

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
