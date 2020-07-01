import os
from kissconfig import ArgumentParser, KissConfig, ConfigFile

pn  = "/tmp/abc/def/geh"
if not os.path.exists(pn):
    os.makedirs(pn)

file1 = "/tmp/abc/a.conf"
file2 = "/tmp/abc/def/b.conf"
file3 = "/tmp/abc/def/geh/c.conf"

open(file1, 'w').write("key: 1")
open(file2, 'w').write("key: 2")
open(file3, 'w').write("key: 3")

myconf = KissConfig()

# searching file to load
myconf.append(ConfigFile(name_pattern_list=["c.conf"],
                         path_list=["/tmp/abc/def/geh", "/tmp/abc/def", "/tmp/abc"]))
myconf.commit()
print(myconf.summary())
#print("key ==> {}".format(myconf.key))


