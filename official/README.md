## Prerequisites

In order to provide examples for PySide2 and PyQt5 I have used [`Qt.py`](https://github.com/mottosso/Qt.py):

```console
python -m pip install Qt.py
```

In some of the examples it is necessary to use classes or functions that are not provided by PyQt5 or PySide2, so the [`qmissings`](https://github.com/eyllanesc/qmissings) module must be used, for this follow the [documentation](https://eyllanesc.github.io/qmissings/installation.html).

## Conversion

To convert the Qt.py examples to PyQt5 you must replace:


| Qt.py    | PyQt5        |
| -------- | ------------ |
| Signal   | pyqtSignal   |
| Slot     | pyqtSlot     |
| Property | pyqtProperty |

## Modules

### Qt Core

| Name                                                 | Link                                                              |
| ---------------------------------------------------- | ----------------------------------------------------------------- |
| [sharedmemory](corelib/ipc/sharedmemory)             | https://doc.qt.io/qt-5/qtcore-ipc-sharedmemory-example.html       |
| [localfortuneclient](corelib/ipc/localfortuneclient) | https://doc.qt.io/qt-5/qtcore-ipc-localfortuneclient-example.html |
| [localfortuneserver](corelib/ipc/localfortuneserver) | https://doc.qt.io/qt-5/qtcore-ipc-localfortuneserver-example.html |

### Qt Charts

| Name                                        | Link                                                          |
| ------------------------------------------- | ------------------------------------------------------------- |
| [areachart](charts/areachart)               | https://doc.qt.io/qt-5/qtcharts-areachart-example.html        |
| [audio](charts/audio)                       | https://doc.qt.io/qt-5/qtcharts-audio-example.html            |
| [barchart](charts/barchart)                 | https://doc.qt.io/qt-5/qtcharts-barchart-example.html         |
| [barmodelmapper](charts/barmodelmapper)     | https://doc.qt.io/qt-5/qtcharts-barmodelmapper-example.html   |
| [boxplotchart](charts/boxplotchart)         | https://doc.qt.io/qt-5/qtcharts-boxplotchart-example.html     |
| [callout](charts/callout)                   | https://doc.qt.io/qt-5/qtcharts-callout-example.html          |
| [candlestickchart](charts/candlestickchart) | https://doc.qt.io/qt-5/qtcharts-candlestickchart-example.html |



### Qt DBus

| Name                      | Link                                                |
| ------------------------- | --------------------------------------------------- |
| [pingpong](dbus/pingpong) | https://doc.qt.io/qt-5/qtdbus-pingpong-example.html |


### Qt Gui

| Name                             | Link                                                   |
| -------------------------------- | ------------------------------------------------------ |
| [rasterwindow](gui/rasterwindow) | https://doc.qt.io/qt-5/qtgui-rasterwindow-example.html |

### Qt Multimedia

| Name                                    | Link                                                                     |
| --------------------------------------- | ------------------------------------------------------------------------ |
| [audiodevices](multimedia/audiodevices) | https://doc.qt.io/qt-5/qtmultimedia-multimedia-audiodevices-example.html |

### Qt Network

| Name                                   | Link                                                        |
| -------------------------------------- | ----------------------------------------------------------- |
| [googlesuggest](network/googlesuggest) | https://doc.qt.io/qt-5/qtnetwork-googlesuggest-example.html |
| [loopback](network/loopback)           | https://doc.qt.io/qt-5/qtnetwork-loopback-example.html      |

### Qt SerialPort

| Name                                  | Link                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| [cenumerator](serialport/cenumerator) | https://doc.qt.io/qt-5/qtserialport-cenumerator-example.html |
| [enumerator](serialport/enumerator)   | https://doc.qt.io/qt-5/qtserialport-enumerator-example.html  |

### Qt Sql

| Name                                   | Link                                                      |
| -------------------------------------- | --------------------------------------------------------- |
| [achedtable](sql/cachedtable)          | https://doc.qt.io/qt-5/qtsql-cachedtable-example.html     |
| [drilldown](sql/drilldown)             | https://doc.qt.io/qt-5/qtsql-drilldown-example.html       |
| [sqlwidgetmapper](sql/sqlwidgetmapper) | https://doc.qt.io/qt-5/qtsql-sqlwidgetmapper-example.html |

## Qt Quick Controls 2

| Name                                              | Link                                                                    |
| ------------------------------------------------- | ----------------------------------------------------------------------- |
| [automotive](quickcontrols2/imagine/automotive)   | https://doc.qt.io/qt-5/qtquickcontrols-imagine-automotive-example.html  |
| [flatstyle](quickcontrols2/flatstyle)             | https://doc.qt.io/qt-5/qtquickcontrols-flatstyle-example.html           |
| [gallery](quickcontrols2/gallery)                 | https://doc.qt.io/qt-5/qtquickcontrols-gallery-example.html             |
| [musicplayer](quickcontrols2/imagine/musicplayer) | https://doc.qt.io/qt-5/qtquickcontrols-imagine-musicplayer-example.html |
| [swipetoremove](quickcontrols2/swipetoremove)     | https://doc.qt.io/qt-5/qtquickcontrols-swipetoremove-example.html       |

### Qt WebEngine

| Name                                     | Link                                                                    |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| [customdialogs](webengine/customdialogs) | https://doc.qt.io/qt-5/qtwebengine-webengine-customdialogs-example.html |
| [lifecycle](webengine/lifecycle)         | https://doc.qt.io/qt-5/qtwebengine-webengine-lifecycle-example.html     |
| [minimal](webengine/minimal)             | https://doc.qt.io/qt-5/qtwebengine-webengine-minimal-example.html       |
| [recipebrowser](webengine/recipebrowser) | https://doc.qt.io/qt-5/qtwebengine-webengine-recipebrowser-example.html |

### Qt WebEngine Widgets


| Name                                                        | Link                                                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [contentmanipulation](webenginewidgets/contentmanipulation) | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-contentmanipulation-example.html |
| [cookiebrowser](webenginewidgets/cookiebrowser)             | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-cookiebrowser-example.html       |
| [html2pdf](webenginewidgets/html2pdf)                       | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-html2pdf-example.html            |
| [maps](webenginewidgets/maps)                               | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-maps-example.html                |
| [markdowneditor](webenginewidgets/markdowneditor)           | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-markdowneditor-example.html      |
| [minimal](webenginewidgets/minimal)                         | https://doc.qt.io/qt-5.9/qtwebengine-webenginewidgets-minimal-example.html           |
| [notifications](webenginewidgets/notifications)             | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-notifications-example.html       |
| [printme](webenginewidgets/printme)                         | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-printme-example.html             |
| [spellchecker](webenginewidgets/spellchecker)               | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-spellchecker-example.html        |
| [webui](webenginewidgets/webui)                             | https://doc.qt.io/qt-5/qtwebengine-webenginewidgets-webui-example.html               |


### Embedded

| Name                                  | Link                                                                      |
| ------------------------------------- | ------------------------------------------------------------------------- |
| [lightmaps](embedded/lightmaps)       | https://code.qt.io/cgit/qt/qtbase.git/tree/examples/embedded/lightmaps    |
| [styleexample](embedded/styleexample) | https://code.qt.io/cgit/qt/qtbase.git/tree/examples/embedded/styleexample |


### Qt Quick Demos

| Name                               | Link                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| [calqlatr](demos/calqlatr)         | https://doc.qt.io/qt-5/qtdoc-demos-calqlatr-example.html     |
| [clocks](demos/clocks)             | https://doc.qt.io/qt-5/qtdoc-demos-clocks-example.html       |
| [coffee](demos/coffee)             | https://doc.qt.io/qt-5/qtdoc-demos-coffee-example.html       |
| [maroon](demos/maroon)             | https://doc.qt.io/qt-5/qtdoc-demos-maroon-example.html       |
| [photosurface](demos/photosurface) | https://doc.qt.io/qt-5/qtdoc-demos-photosurface-example.html |

