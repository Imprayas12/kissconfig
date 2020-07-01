import os
from kissconfig import KissConfig, ArgumentParser, EnvValue, Load


myconf = KissConfig()
filename = 'site_x.yml'

# environment valuable
myconf.append(EnvValue())
myconf.append(Load(filename))
myconf.append(dict(a=1, b=2))

myconf.commit()
print(myconf.summary())

# access value in site_x.yml
print(myconf.xxx_param)
# 123 

