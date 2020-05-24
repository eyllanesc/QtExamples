from functools import partial

from PyQt5.QtCore import QCoreApplication, Qt, QUrl
from PyQt5.QtWidgets import QAction, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

import spellchecker_rc  # noqa: F401


class WebView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_spellCheckLanguages = dict()
        self.m_spellCheckLanguages["English"] = "en-US"
        self.m_spellCheckLanguages["German"] = "de-DE"
        profile = self.page().profile()
        profile.setSpellCheckEnabled(True)
        profile.setSpellCheckLanguages(("en-US",))

    def contextMenuEvent(self, event):
        data = self.page().contextMenuData()
        assert data.isValid()

        if not data.isContentEditable():
            super().contextMenuEvent(event)
            return

        profile = self.page().profile()
        languages = profile.spellCheckLanguages()
        menu = self.page().createStandardContextMenu()
        menu.setParent(self)
        menu.addSeparator()

        spellcheckAction = QAction(self.tr("Check Spelling"), None)
        spellcheckAction.setCheckable(True)
        spellcheckAction.setChecked(profile.isSpellCheckEnabled())
        spellcheckAction.toggled.connect(profile.setSpellCheckEnabled)
        menu.addAction(spellcheckAction)
        if profile.isSpellCheckEnabled():
            subMenu = menu.addMenu(self.tr("Select Language"))
            for key, lang in self.m_spellCheckLanguages.items():
                action = subMenu.addAction(key)
                action.setCheckable(True)
                action.setChecked(lang in languages)
                action.triggered.connect(partial(self.on_triggered, lang))
        menu.aboutToHide.connect(menu.deleteLater)
        menu.popup(event.globalPos())

    def on_triggered(self, lang):
        profile = self.page().profile()
        profile.setSpellCheckLanguages((lang,))


def main():
    import os
    import sys

    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    os.environ["QTWEBENGINE_DICTIONARIES_PATH"] = os.path.join(
        CURRENT_DIR, "qtwebengine_dictionaries"
    )

    QCoreApplication.setOrganizationName("QtExamples")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    view = WebView()
    view.setUrl(QUrl("qrc:/index.html"))
    view.resize(500, 640)
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
