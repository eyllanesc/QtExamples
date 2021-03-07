# -*- coding: utf-8 -*-
import os.path

from PySide2.QtQml import qmlRegisterType

from .filters import _filters
from .sources import _sources


def register_types(uri="qutevideo", version_mayor=1, version_minor=0):
    for cls, name in _filters | _sources:
        qmlRegisterType(cls, uri, version_mayor, version_minor, name)


def _fix_qt_plugin_path():
    import PySide2

    dirname = os.path.dirname(PySide2.__file__)
    plugin_path = os.path.join(dirname, "plugins", "platforms")
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path


_fix_qt_plugin_path()

del _fix_qt_plugin_path
