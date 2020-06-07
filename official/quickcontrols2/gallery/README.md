[QQuickStyle](https://doc.qt.io/qt-5/qquickstyle.html) is not available in either [PyQt5](https://pypi.org/project/PyQt5/) or [PySide2](https://pypi.org/project/PySide2/) so I have created a wrapper using [pybind11](https://github.com/pybind/pybind11) so you have to compile [the project](../../../additionals/fakequickcontrols2/):

```bash
cd additionals/fakequickcontrols2
mkdir build && cd build
cmake ..
make
```

and copy the .so to the side of `main.py`.