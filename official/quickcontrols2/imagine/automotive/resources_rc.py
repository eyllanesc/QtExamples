# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.15.0)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x00\x80\
\x5b\
\x43\x6f\x6e\x74\x72\x6f\x6c\x73\x5d\x0a\x53\x74\x79\x6c\x65\x3d\
\x49\x6d\x61\x67\x69\x6e\x65\x0a\x0a\x5b\x49\x6d\x61\x67\x69\x6e\
\x65\x5d\x0a\x50\x61\x74\x68\x3d\x3a\x2f\x69\x6d\x61\x67\x69\x6e\
\x65\x2d\x61\x73\x73\x65\x74\x73\x0a\x0a\x5b\x49\x6d\x61\x67\x69\
\x6e\x65\x5c\x50\x61\x6c\x65\x74\x74\x65\x5d\x0a\x54\x65\x78\x74\
\x3d\x23\x36\x61\x66\x66\x63\x64\x0a\x42\x75\x74\x74\x6f\x6e\x54\
\x65\x78\x74\x3d\x23\x36\x61\x66\x66\x63\x64\x0a\x57\x69\x6e\x64\
\x6f\x77\x54\x65\x78\x74\x3d\x23\x36\x61\x66\x66\x63\x64\x0a\
"

qt_resource_name = b"\
\x00\x15\
\x08\x1e\x16\x66\
\x00\x71\
\x00\x74\x00\x71\x00\x75\x00\x69\x00\x63\x00\x6b\x00\x63\x00\x6f\x00\x6e\x00\x74\x00\x72\x00\x6f\x00\x6c\x00\x73\x00\x32\x00\x2e\
\x00\x63\x00\x6f\x00\x6e\x00\x66\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x72\x8f\xc9\x5e\x32\
"

qt_version = [int(v) for v in QtCore.qVersion().split(".")]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2


def qInitResources():
    QtCore.qRegisterResourceData(
        rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data
    )


def qCleanupResources():
    QtCore.qUnregisterResourceData(
        rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data
    )


qInitResources()
