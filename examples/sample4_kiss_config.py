#coding:utf-8
'''
ランタイム書き込みサンプル.
'''
from kissconfig import ArgumentParser, KissConfig, ConfigFile

myconf = KissConfig()

# loadすべき、ファイル名を直接指定する
myconf.append(ConfigFile("test1.yml"))
myconf.commit()
print(myconf.summary())

# access value in test1.yml の key1
print("before modification: {}".format(myconf.key1))

# access value in test1.yml の key1
#myconf.key1 = 'modified value'
myconf['key1'] = 'modified value'

print("after modification: {}".format(myconf.key1))


