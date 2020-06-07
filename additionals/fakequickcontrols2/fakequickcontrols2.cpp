#include "fakequickcontrols2.h"

#include <QQuickStyle>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

void Fakequickcontrols2::addStylePath(const std::string &path)
{
    return QQuickStyle::addStylePath(QString::fromStdString(path));
}

std::vector<std::string> Fakequickcontrols2::availableStyles()
{
    std::vector<std::string> styles;
    for(const QString & style: QQuickStyle::availableStyles()){
        styles.push_back(style.toStdString());
    }
    return styles;
}

std::string Fakequickcontrols2::name()
{
    return QQuickStyle::name().toStdString();
}

std::string Fakequickcontrols2::path()
{
    return QQuickStyle::path().toStdString();
}

void Fakequickcontrols2::setFallbackStyle(const std::string &style)
{
    QQuickStyle::setFallbackStyle(QString::fromStdString(style));
}

void Fakequickcontrols2::setStyle(const std::string &style)
{
    QQuickStyle::setStyle(QString::fromStdString(style));
}

std::vector<std::string> Fakequickcontrols2::stylePathList()
{
    std::vector<std::string> paths;
    for(const QString & path: QQuickStyle::stylePathList()){
        paths.push_back(path.toStdString());
    }
    return paths;
}

PYBIND11_MODULE(Fakequickcontrols2, m) {
    m.doc() = "Fakequickcontrols2 module";
    m.def("addStylePath", &Fakequickcontrols2::addStylePath);
    m.def("availableStyles", &Fakequickcontrols2::availableStyles);
    m.def("name", &Fakequickcontrols2::name);
    m.def("path", &Fakequickcontrols2::path);
    m.def("setFallbackStyle", &Fakequickcontrols2::setFallbackStyle);
    m.def("setStyle", &Fakequickcontrols2::setStyle);
    m.def("stylePathList", &Fakequickcontrols2::stylePathList);
#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
