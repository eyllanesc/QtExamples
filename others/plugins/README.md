Many of Qt's functionalities are implemented through plugins such as:

- database drivers.
- image formats,
- styles, etc.

That allows to enable the functionalities also in PyQt5 or PySide2.

In general, there are several methods depending on the PyQt5/PySide2 installation.

### 1. Official repositories

If PyQt5/PySide2 was installed using the official OS repositories then it is likely that it will also test the plugin binaries so it is enough to install it using the OS tools.

If it does not provide it then you will have to compile the plugin but using the Qt provided by the OS since it is the one used by the maintainers to compile PyQt5/PySide2

### 2. pip used or manually compiled

You must install Qt of the same version that was used to compile the library, and to find out the version of Qt you must use the following commands:

#### PyQt5

```console
python -c "from PyQt5.QtCore import QT_VERSION_STR; print('Qt version', QT_VERSION_STR)"
```

#### PySide2

```console
python -c "from PySide2.QtCore import qVersion; print('Qt version', qVersion())"
```

To install Qt you can use [aqtinstall](https://github.com/miurahr/aqtinstall).

Then you will have to compile the project and copy the binaries in places similar to the one saved in Qt.

In the case of plugins, it is installed in the QT_INSTALL_PLUGINS folder that can be obtained with qmake to install Qt:

```console
$ qmake -query QT_INSTALL_PLUGINS
```

And for the bindings use:

#### PyQt5
```
python -c "from PyQt5.QtCore import QLibraryInfo; print(QLibraryInfo.location(QLibraryInfo.PluginsPath))"
```

#### PySide2
```
python -c "from PySide2.QtCore import QLibraryInfo; print(QLibraryInfo.location(QLibraryInfo.PluginsPath))"
```
