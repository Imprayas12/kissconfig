Kiss Config
===========

config utility over argparse and yaml/json files.
-------------------------------------------------

tutorial
--------

see examples folder

TODO
----

examples needs to hvae rst doc

NEWS
----

-  0.3.1 – debug log でkey でfile-searchするときのlog.debugを増やした
-  0.3.0 – ConfigFile の key 読み出しに、展開ファイル名機能を追加 – in
   ConfigFile option keyword argument, a filename extraction format
   ``key_extract_format`` is added
-  0.2.1 – argparse value is reflected only when each value is not None.
-  0.2.0 – adding a experimental version of config file search func.

@issue

ConfigFileのパス名の終わりが / という要求は、誤解を生みやすい.
あるとか、ないとか なにを使ったかとか requiredじゃないからスルーしたとか
レポートしたほうがいい.
