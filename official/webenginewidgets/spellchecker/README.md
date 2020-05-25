## GENERATE DICTIONARY

[`qwebengine_convert_dict`](https://code.qt.io/cgit/qt/qtwebengine.git/tree/src/tools/qwebengine_convert_dict) is a tool to convert dic file to bdict that comes with QtWebEngine.

Execute on console:

```
 qwebengine_convert_dict /path/of/filename.dic /path/of/filename.bdic
```
In this case:
```console
$ mkdir qtwebengine_dictionaries
$ qwebengine_convert_dict dict/en/en-US.dic qtwebengine_dictionaries/en-US.bdic
Reading dict/en/en-US.aff
Reading dict/en/en-US.dic
dict/en/en-US.dic_delta not found.
Serializing...
Verifying...
Writing qtwebengine_dictionaries/en-US.bdic
Success. Dictionary converted.
$ qwebengine_convert_dict dict/de/de-DE.dic qtwebengine_dictionaries/de-DE.bdic
Reading dict/de/de-DE.aff
Reading dict/de/de-DE.dic
dict/de/de-DE.dic_delta not found.
Serializing...
Verifying...
Writing qtwebengine_dictionaries/de-DE.bdic
Success. Dictionary converted.
```