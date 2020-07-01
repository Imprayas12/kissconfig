"""
0.3.0 からのファイル名展開処理.

- 0.3.0より以前はどうしたかったか.    sample_platform_old.py

"""

import os
import kissconfig
import platform
import subprocess

tmpfolder = '/tmp'
myfolder = os.path.splitext(__file__)[0]
pathname = os.path.join(tmpfolder, myfolder)

subprocess.run(['mkdir', '-p', '{}'.format(pathname)])
open(os.path.join(pathname, 'xxx_default.yml'), 'w').write('in: i_am_unknown')
open(os.path.join(pathname, 'xxx_linux.yml'), 'w').write('in: i_am_linux')
open(os.path.join(pathname, 'xxx_darwin.yml'), 'w').write('in: i_am_darwin')


pl = dict(os=platform.system().lower(), node=platform.node().lower(), release=platform.release(), version=platform.version(), machine=platform.machine().lower())

# confg を osで切り替える処理.
# macならdarwin
'''
key_extract_format='config_{os}.yml',

Macなら
config_darwin.yml
Linuxなら
config_linux.yml
を読み出す処理.
'''
cfg = kissconfig.KissConfig()
cfg.append(pl)
# 直接読む.
cfg.append(kissconfig.ConfigFile('xxx_default.yml', path_list=[pathname], require=True))
# osのkeyに相当するファイル名を読む.
cfg.append(kissconfig.ConfigFile(key='os', key_extract_format='xxx_{os}.yml', path_list=[pathname], require=True))

cfg.commit()

print(cfg.summary())
'''

cfg.append(kissconfig.ConfigFile(key='os', key_extract_format='config_{os}.yml', require=True))

元レイヤーでosを認識し
dict(os=platform.system().lower())

ConfigFileで以下のファイルをosによって読み替える.
config_darwin.yml
config_linux.yml
config_windows.yml


'''

