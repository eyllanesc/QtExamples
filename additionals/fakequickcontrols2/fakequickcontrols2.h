#ifndef FAKEQUICKCONTROLS2_H
#define FAKEQUICKCONTROLS2_H

#include <string>
#include <vector>

class Fakequickcontrols2
{
public:
    static void addStylePath(const std::string &path);
    static std::vector<std::string> availableStyles();
    static std::string name();
    static std::string path();
    static void	setFallbackStyle(const std::string &style);
    static void	setStyle(const std::string &style);
    static std::vector<std::string> stylePathList();
};

#endif // FAKEQUICKCONTROLS2_H
