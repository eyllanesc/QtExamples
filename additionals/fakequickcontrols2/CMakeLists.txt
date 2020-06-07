cmake_minimum_required(VERSION 3.5)

project(Fakequickcontrols2 LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 COMPONENTS QuickControls2 REQUIRED)
add_definitions(-DQT_NO_KEYWORDS)

find_package(pybind11)

pybind11_add_module(Fakequickcontrols2 fakequickcontrols2.cpp)

target_link_libraries(Fakequickcontrols2 PRIVATE Qt5::QuickControls2)
