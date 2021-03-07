# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET

from lib import SuggestionCompleter, SuggestionNetworkModel

from PyQt5.QtCore import Qt, QUrl, QUrlQuery
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import QApplication, QLineEdit


class SearchSuggestionModel(SuggestionNetworkModel):
    def create_request(self, text):
        url = QUrl("http://toolbarqueries.google.com/complete/search")
        query = QUrlQuery()
        query.addQueryItem("q", text)
        query.addQueryItem("output", "toolbar")
        query.addQueryItem("hl", "en")
        url.setQuery(query)
        request = QNetworkRequest(url)
        return request

    def process_reply(self, reply):
        results = []
        error_string = ""
        if reply.error() == QNetworkReply.NoError:
            content = reply.readAll().data()
            suggestions = ET.fromstring(content)
            for data in suggestions.iter("suggestion"):
                results.append(data.attrib["data"])
        elif reply.error() != QNetworkReply.OperationCanceledError:
            error_string = reply.errorString()
        return results, error_string


def main():
    app = QApplication(sys.argv)

    searchbar = QLineEdit()
    completer = SuggestionCompleter(caseSensitivity=Qt.CaseInsensitive)
    model = SearchSuggestionModel()
    completer.setModel(model)
    searchbar.setCompleter(completer)
    searchbar.resize(640, 60)
    searchbar.show()

    ret = app.exec_()
    sys.exit(ret)


if __name__ == "__main__":
    main()
