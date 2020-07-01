from kissconfig import KissConfig, ConfigFile
import chardet
from pprint import pprint
def test_kanji():

        config = KissConfig()
        
        config.append(ConfigFile('site_x.yml'))
        value = config.commit()
        pprint(value)


test_kanji()        
