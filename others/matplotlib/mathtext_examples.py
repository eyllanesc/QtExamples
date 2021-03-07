# -*- coding: utf-8 -*-
# https://matplotlib.org/3.2.1/gallery/text_labels_and_annotations/mathtext_examples.html

import re
import subprocess
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication

# Selection of features following "Writing mathematical expressions" tutorial
mathtext_titles = {
    0: "Header demo",
    1: "Subscripts and superscripts",
    2: "Fractions, binomials and stacked numbers",
    3: "Radicals",
    4: "Fonts",
    5: "Accents",
    6: "Greek, Hebrew",
    7: "Delimiters, functions and Symbols",
}
n_lines = len(mathtext_titles)

# Randomly picked examples
mathext_demos = {
    0: r"$W^{3\beta}_{\delta_1 \rho_1 \sigma_2} = "
    r"U^{3\beta}_{\delta_1 \rho_1} + \frac{1}{8 \pi 2} "
    r"\int^{\alpha_2}_{\alpha_2} d \alpha^\prime_2 \left[\frac{ "
    r"U^{2\beta}_{\delta_1 \rho_1} - \alpha^\prime_2U^{1\beta}_"
    r"{\rho_1 \sigma_2} }{U^{0\beta}_{\rho_1 \sigma_2}}\right]$",
    1: r"$\alpha_i > \beta_i,\ "
    r"\alpha_{i+1}^j = {\rm sin}(2\pi f_j t_i) e^{-5 t_i/\tau},\ "
    r"\ldots$",
    2: r"$\frac{3}{4},\ \binom{3}{4},\ \genfrac{}{}{0}{}{3}{4},\ "
    r"\left(\frac{5 - \frac{1}{x}}{4}\right),\ \ldots$",
    3: r"$\sqrt{2},\ \sqrt[3]{x},\ \ldots$",
    4: r"$\mathrm{Roman}\ , \ \mathit{Italic}\ , \ \mathtt{Typewriter} \ "
    r"\mathrm{or}\ \mathcal{CALLIGRAPHY}$",
    5: r"$\acute a,\ \bar a,\ \breve a,\ \dot a,\ \ddot a, \ \grave a, \ "
    r"\hat a,\ \tilde a,\ \vec a,\ \widehat{xyz},\ \widetilde{xyz},\ "
    r"\ldots$",
    6: r"$\alpha,\ \beta,\ \chi,\ \delta,\ \lambda,\ \mu,\ "
    r"\Delta,\ \Gamma,\ \Omega,\ \Phi,\ \Pi,\ \Upsilon,\ \nabla,\ "
    r"\aleph,\ \beth,\ \daleth,\ \gimel,\ \ldots$",
    7: r"$\coprod,\ \int,\ \oint,\ \prod,\ \sum,\ "
    r"\log,\ \sin,\ \approx,\ \oplus,\ \star,\ \varpropto,\ "
    r"\infty,\ \partial,\ \Re,\ \leftrightsquigarrow, \ \ldots$",
}


def doall():
    import sys

    app = QApplication(sys.argv)

    fig = Figure(figsize=(6, 7))
    canvas = FigureCanvas(fig)
    canvas.resize(640, 480)
    canvas.show()

    # Colors used in Matplotlib online documentation.
    mpl_blue_rvb = (191.0 / 255.0, 209.0 / 256.0, 212.0 / 255.0)
    mpl_orange_rvb = (202.0 / 255.0, 121.0 / 256.0, 0.0 / 255.0)
    mpl_grey_rvb = (51.0 / 255.0, 51.0 / 255.0, 51.0 / 255.0)

    # Creating figure and axis
    fig.add_axes([0.01, 0.01, 0.98, 0.90], facecolor="white", frameon=True)
    ax = fig.subplots()
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_title(
        "Matplotlib's math rendering engine",
        color=mpl_grey_rvb,
        fontsize=14,
        weight="bold",
    )
    ax.set_xticklabels("", visible=False)
    ax.set_yticklabels("", visible=False)

    # Gap between lines in axes coords
    line_axesfrac = 1.0 / (n_lines)

    # Plotting header demonstration formula
    full_demo = mathext_demos[0]
    ax.annotate(
        full_demo,
        xy=(0.5, 1.0 - 0.59 * line_axesfrac),
        color=mpl_orange_rvb,
        ha="center",
        fontsize=20,
    )

    # Plotting features demonstration formulae
    for i_line in range(1, n_lines):
        baseline = 1 - (i_line) * line_axesfrac
        baseline_next = baseline - line_axesfrac
        title = mathtext_titles[i_line] + ":"
        fill_color = ["white", mpl_blue_rvb][i_line % 2]
        ax.fill_between(
            [0.0, 1.0],
            [baseline, baseline],
            [baseline_next, baseline_next],
            color=fill_color,
            alpha=0.5,
        )
        ax.annotate(
            title,
            xy=(0.07, baseline - 0.3 * line_axesfrac),
            color=mpl_grey_rvb,
            weight="bold",
        )
        demo = mathext_demos[i_line]
        ax.annotate(
            demo,
            xy=(0.05, baseline - 0.75 * line_axesfrac),
            color=mpl_grey_rvb,
            fontsize=16,
        )

    for i in range(n_lines):
        s = mathext_demos[i]
        print(i, s)

    sys.exit(app.exec_())


if "--latex" in sys.argv:
    # Run: python mathtext_examples.py --latex
    # Need amsmath and amssymb packages.
    fd = open("mathtext_examples.ltx", "w")
    fd.write("\\documentclass{article}\n")
    fd.write("\\usepackage{amsmath, amssymb}\n")
    fd.write("\\begin{document}\n")
    fd.write("\\begin{enumerate}\n")

    for i in range(n_lines):
        s = mathext_demos[i]
        s = re.sub(r"(?<!\\)\$", "$$", s)
        fd.write("\\item %s\n" % s)

    fd.write("\\end{enumerate}\n")
    fd.write("\\end{document}\n")
    fd.close()

    subprocess.call(["pdflatex", "mathtext_examples.ltx"])
else:
    doall()
