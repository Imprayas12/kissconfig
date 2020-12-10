import os
from kissconfig import ArgumentParser, KissConfig, ConfigFile

pn  = "/tmp/kissconfig_test"
if not os.path.exists(pn):
    os.makedirs(pn)

file1 = os.path.join(pn, "a.conf")
file2 = os.path.join(pn, "b.conf")
open(file1, 'w').write("key: 1")
open(file2, 'w').write("key: 2")

conf = KissConfig()
# default
conf.append(dict(filename="a.conf"))

# user specification
parser = ArgumentParser()
parser.add_argument("-f", "--filename")
conf.append(parser.parse_args())

conf.append(ConfigFile(key='filename', path_list=[pn], required=True))

conf.commit()
print(conf.summary())


'''
$ python3 sample6_kiss_config.py
<class 'kissconfig.kiss_config.KissConfig'>
- - filename
  - a.conf
- - key
  - 1

$ python3 sample6_kiss_config.py --filename=b.conf
<class 'kissconfig.kiss_config.KissConfig'>
- - filename
  - b.conf
- - key
  - 2
'''

