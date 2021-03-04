from collections.abc import Iterable
from functools import cached_property
from typing import List, Optional, Tuple

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QEventLoop, QObject
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import QCompleter


class SuggestionNetworkModel(QStandardItemModel):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._current_reply: Optional[QNetworkReply] = None
        self._error_string: str = ""
        self.network_manager.finished.connect(self.handle_finished)

    @cached_property
    def network_manager(self) -> QNetworkAccessManager:
        return QNetworkAccessManager()

    @property
    def error_string(self) -> str:
        return self._error_string

    @pyqtSlot(str)
    def search(self, text: str) -> None:
        self.clear()
        if self._current_reply is not None:
            self._current_reply.abort()
        self._current_reply = None
        if text:
            r = self.create_request(text)
            self._current_reply = self.network_manager.get(r)

        loop = QEventLoop()
        self.finished.connect(loop.quit)
        loop.exec_()

    def create_request(self, text: str) -> QNetworkRequest:
        request = QNetworkRequest()
        return request

    @pyqtSlot(QNetworkReply)
    def handle_finished(self, reply: QNetworkReply) -> None:
        reply.deleteLater()
        if reply is not self._current_reply:
            return
        if reply.error() == QNetworkReply.OperationCanceledError:
            return
        results, error_string = self.process_reply(reply)
        if isinstance(results, Iterable):
            for result in results:
                item = QStandardItem(result)
                self.appendRow(item)
        if isinstance(error_string, str) and error_string:
            self._error_string = error_string
        else:
            self._error_string = ""
        self._current_reply = None
        self.finished.emit()

    def process_reply(self, reply: QNetworkReply) -> Tuple[List[str], str]:
        return [], reply.errorString()


class SuggestionCompleter(QCompleter):
    def splitPath(self, path: str) -> List[str]:
        if not isinstance(self.model(), SuggestionNetworkModel):
            raise TypeError(f"error {SuggestionNetworkModel}")
        self.model().search(path.strip())
        return super().splitPath(path)
