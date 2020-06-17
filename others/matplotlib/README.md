Many times it is required to embed matplotlib with Qt since it allows to use many more types of widgets or to use the other Qt modules. And fortunately matplotlib provides Qt as a backend, but unfortunately the official examples (see official example [here](https://matplotlib.org/3.2.1/gallery/user_interfaces/embedding_in_qt_sgskip.html)) are limited so this post will try to provide examples and basic tips on how both libraries should interact.

The following rules are basic:

- The binding (PyQt5 or PySide2) must be imported first so that matplotlib that library must use internally.

- You should not use [`matplotlib.pyplot`](https://matplotlib.org/users/pyplot_tutorial.html) but [`Figure`](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.figure.Figure.html) to manipulate the painting and the FigureCanvas as a widget.

Many functions or classes accept an `AxesSubplot` as a parameter (with the argument "ax") so it must be used to point to the axis where it should be drawn.

### Sample plots
| Example                                                                            | Link                                                                              |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [Simple Plot](simple_plot.py)                                                      | https://matplotlib.org/gallery/lines_bars_and_markers/simple_plot.html            |
| [Multiple subplots](subplot.py)                                                    | https://matplotlib.org/gallery/subplots_axes_and_figures/subplot.html             |
| [Image Demo](image_demo.py)                                                        | https://matplotlib.org/gallery/images_contours_and_fields/image_demo.html         |
| [pcolormesh](pcolormesh_levels.py)                                                 | https://matplotlib.org/gallery/images_contours_and_fields/pcolormesh_levels.html  |
| [Demo of the histogram (hist) function with a few features](histogram_features.py) | https://matplotlib.org/gallery/statistics/histogram_features.html                 |
| [PathPatch object](path_patch.py)                                                  | https://matplotlib.org/gallery/shapes_and_collections/path_patch.html             |
| [3D surface (color map](surface3d.py)                                              | https://matplotlib.org/gallery/mplot3d/surface3d.html                             |
| [Streamplot](plot_streamplot.py)                                                   | https://matplotlib.org/gallery/images_contours_and_fields/plot_streamplot.html    |
| [Ellipse Demo](ellipse_demo.py)                                                    | https://matplotlib.org/gallery/shapes_and_collections/ellipse_demo.html           |
| [Percentiles as horizontal bar chart](barchart_demo.py)                            | https://matplotlib.org/gallery/statistics/barchart_demo.html                      |
| [Basic pie chart](pie_features.py)                                                 | https://matplotlib.org/gallery/pie_and_polar_charts/pie_features.html             |
| [Table Demo](table_demo.py)                                                        | https://matplotlib.org/gallery/misc/table_demo.html                               |
| [Scatter Demo2](scatter_demo2.py)                                                  | https://matplotlib.org/gallery/lines_bars_and_markers/scatter_demo2.html          |
| [Filled polygon](fill.py)                                                          | https://matplotlib.org/gallery/lines_bars_and_markers/fill.html                   |
| [Date tick labels](date.py)                                                        | https://matplotlib.org/gallery/text_labels_and_annotations/date.html              |
| [Log Demo](log_demo.py)                                                            | https://matplotlib.org/gallery/scales/log_demo.html                               |
| [Polar Demo](polar_demo.py)                                                        | https://matplotlib.org/gallery/pie_and_polar_charts/polar_demo.html               |
| [Legend using pre-defined labels](legend.py)                                       | https://matplotlib.org/gallery/text_labels_and_annotations/legend.html            |
| [Mathtext Examples](mathtext_examples.py)                                          | https://matplotlib.org/gallery/text_labels_and_annotations/mathtext_examples.html |
| [Rendering math equation using TeX](tex_demo.py)                                   | https://matplotlib.org/gallery/text_labels_and_annotations/tex_demo.html          |
| [Subplot example](Subplot.py)                                                      | https://matplotlib.org/tutorials/introductory/sample_plots.html#subplot-example   |


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
