---
name: Request Example
about: Ask for a custom example
title: "[Example]"
labels: request for example
assignees: ''

---

**Describe the custom example**

Clearly indicate the custom example by stating the behavior in detail.

**Images**

If applicable, add images that describe what you want to get.

**Environment:**
- OS
- Python version:  `python --version`
- PyQt5/PySide2 version: 

    ##### PyQt5
    ```
    python -c "from PyQt5.QtCore import PYQT_VERSION_STR; print('PyQt5 version', PYQT_VERSION_STR)"
    python -c "from PyQt5.QtCore import QT_VERSION_STR; print('Qt version', QT_VERSION_STR)"
    ```
    ##### PySide2
    ```
    python -c "from PySide2 import __version__; print('PySide2 version', __version__)"
    python -c "from PySide2.QtCore import qVersion; print('Qt version', qVersion())"
    ```
