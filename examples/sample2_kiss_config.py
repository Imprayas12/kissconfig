import os
import logging as log
log.basicConfig(level=log.DEBUG)
from kissconfig import KissConfig, ConfigFile, ArgumentParser

myconf = KissConfig()

"""
この場合

ConfigFile の名前は   version という keyのデータ名がファイル名として使われる.
ConfigFileを指定した時点では、test1.yml が指定されているので test1.ymlの内容が読み出される.

myconf.append(dict(version="test1.yml"))
myconf.append(ConfigFile(key='version'))
myconf.append(dict(version="test2.yml"))
conf = myconf.commit()


この場合はConfigFileを二度呼び出しているが二度目のファイル名はtest2.ymlになる.

myconf.append(dict(version="test1.yml"))
myconf.append(ConfigFile(key='version'))
myconf.append(dict(version="test2.yml"))
myconf.append(ConfigFile(key='version'))

"""
myconf.append(dict(version="test1.yml"))
myconf.append(ConfigFile(key='version'))
myconf.append(dict(version="test2.yml"))
myconf.append(ConfigFile(key='version'))
conf = myconf.commit()

log.debug(conf.summary())

