Many times it is required to embed matplotlib with Qt since it allows to use many more types of widgets or to use the other Qt modules. And fortunately matplotlib provides Qt as a backend, but unfortunately the official examples (see official example [here](https://matplotlib.org/3.2.1/gallery/user_interfaces/embedding_in_qt_sgskip.html)) are limited so this post will try to provide examples and basic tips on how both libraries should interact.

The following rules are basic:

- The binding (PyQt5 or PySide2) must be imported first so that matplotlib that library must use internally.

- You should not use [`matplotlib.pyplot`](https://matplotlib.org/users/pyplot_tutorial.html) but [`Figure`](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.figure.Figure.html) to manipulate the painting and the FigureCanvas as a widget.

Many functions or classes accept an `AxesSubplot` as a parameter (with the argument "ax") so it must be used to point to the axis where it should be drawn.

### matplotlib widgets

In this section I show the translation of the official examples of the matplotlib widgets from [`matplotlib.pyplot`](https://matplotlib.org/users/pyplot_tutorial.html) to Qt.

| Widget                                                | Link                                                             |
| ----------------------------------------------------- | ---------------------------------------------------------------- |
| [buttons](widgets/buttons.py)                         | https://matplotlib.org/examples/widgets/buttons.html             |
| [check_buttons](widgets/check_buttons.py)             | https://matplotlib.org/examples/widgets/check_buttons.html       |
| [cursor](widgets/cursor.py)                           | https://matplotlib.org/examples/widgets/cursor.html              |
| [lasso_selector_demo](widgets/lasso_selector_demo.py) | https://matplotlib.org/examples/widgets/lasso_selector_demo.html |
| [menu](widgets/menu.py)                               | https://matplotlib.org/examples/widgets/menu.html                |
| [multicursor](widgets/multicursor.py)                 | https://matplotlib.org/examples/widgets/multicursor.html         |
| [radio_buttons](widgets/radio_buttons.py)             | https://matplotlib.org/examples/widgets/radio_buttons.html       |
| [rectangle_selector](widgets/rectangle_selector.py)   | https://matplotlib.org/examples/widgets/rectangle_selector.html  |
| [slider_demo](widgets/slider_demo.py)                 | https://matplotlib.org/examples/widgets/slider_demo.html         |
| [span_selector](widgets/span_selector.py)             | https://matplotlib.org/examples/widgets/span_selector.html       |
