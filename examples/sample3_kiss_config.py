from kissconfig import ArgumentParser, KissConfig, ConfigFile

myconf = KissConfig()

# loadすべき、ファイル名を直接指定する
myconf.append(ConfigFile("test1.yml"))
myconf.commit()
print(myconf.summary())

# access value in test1.yml の key1
print("key1 ==> {}".format(myconf.key1))


