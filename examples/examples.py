

'''派生層から基本層の変数にアクセスして、派生層のための変数を構成する場合.
    configがprodかstageかで、ファイル名パラメーターを生成する場合等.'''

if __name__ == '__main__0':
    
    import kissconfig as cfg
    config = cfg.KissConfig()
    # 基本設定.
    config.append(dict(mode='prod'))
    # あるconfig値を得て、別のconfig値を生成して設定する
    current_mode_value = config.get('mode')
    # 派生からの派生設定
    config.append(dict(mode_file_name="mode_{}.json".format(current_mode_value)))
    # 確定.
    values = config.commit()
    # config値アクセス.
    print("values are {} ".format([(k, values[k]) for k in values]))

if __name__ == '__main__0':
    '''
    デフォルトは production だけど、 コマンドラインで prod / stage / dev の切り替えを指定し、得られた文字列変数をファイル名に使う
    '''
    import kissconfig as cfg
    config = cfg.KissConfig()
    parser = cfg.ArgumentParser()

    # 基本設定.
    config.append(dict(mode='prod'))
    # 派生設定  コマンドライン
    parser.add_argument("-m", "--mode", choices=['prod', 'stage', 'dev'], default='prod')
    args = parser.parse_args()
    config.append(args)
    # あるconfig値を得て、別のconfig値を生成して設定する
    current_mode_value = config.get('mode')
    # 派生からの派生設定
    config.append(dict(mode_file_name="mode_{}.json".format(current_mode_value)))
    # 確定.
    values = config.commit()
    # config値へのアクセス.
    print("values are {} ".format([(k, values[k]) for k in values]))

if __name__ == '__main__0':
    import kissconfig as cfg

    print(' -- organized indirect config file which specified by arguments')

    config = cfg.KissConfig()
    parser = cfg.ArgumentParser()

    # the 1st (lowest and base) layer: default static values 
    config.append(dict(verbose=False))
    config.append(dict(xxx_param=3.1415926))
    config.append(dict(mode='prod'))
    # the 2nd layer: cmd line
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-e", "--epsilon", default=2.7182818)
    parser.add_argument("-m", "--mode", choices=['prod', 'stage', 'dev'], default='prod')
    args = parser.parse_args()
    config.append(args)
    # the 3rd layer: static file by 
    config.append(cfg.ConfigFile(key='mode', required=True))
    values = config.commit()
    print("values are {} ".format([(k, values[k]) for k in values]))
    print("usage verbose={} ".format(values.verbose))

if __name__ == '__main__0':
    import sys
    def test_0():
        print(' -- usecase0: initialize')
        config = KissConfig()
        value = config.commit()
        pprint(value)

    def test_1():
        print(' -- usecase1: default layer and ArgumentParser layeer')
        config = KissConfig()
        # the 1st (lowest) layer
        config.append(dict(verbose=False))
        # the 2nd layer
        parser = ArgumentParser()
        parser.add_argument("-v", "--verbose", action='store_true')
        args = parser.parse_args(['--verbose'])
        config.append(args)
        value = config.commit()
        pprint(value)

    def test_2():
        print(' -- usecase2 single config file')
        config = KissConfig()
        config.append(ConfigFile('site_x.yml'))
        value = config.commit()
        pprint(value)

    def test_2_a():
        print(' -- usecase2_a single config file')
        config = KissConfig()
        config.append(ConfigFile('site_x_a.yml'))
        value = config.commit()
        pprint(value['wifi']['ssid'])
        pprint("-- config.wifi: <<{}>>".format(config.wifi))
        pprint("-- config.wifi: <<{}>>".format(config.wifi.ssid))

    def test_3():
        print(' -- usecase3 indirect config file which specified by arguments')
        config = KissConfig()
        # the 1st (lowest) layer
        config.append(dict(configfile='default_x.yml'))
        # the 2nd layer
        parser = ArgumentParser() # for hard coded arguments
        parser.add_argument("-f", "--configfile")
        args = parser.parse_args(['--configfile=site_x.yml'])
        config.append(args)
        config.append(ConfigFile(key='configfile'))
        value = config.commit()
        pprint("{} {}".format('xxx_param', config['xxx_param']))

    def test_3_error():
        '''
        specified value with key does not found
        '''
        print(' -- usecase3_error: indirect config file which specified by arguments and the file does not exist')
        config = KissConfig()
        # the 1st (lowest) layer
        config.append(dict(configfile='a_missing_file.yml'))
        config.append(ConfigFile(key='configfile', required=True))
        try:
            value = config.commit()
        except FileNotFoundError:
            log.debug("expected FileNotFoundError")
        try:
            pprint("{} {}".format('xxx_param', config['xxx_param']))
        except KeyError:
            log.debug("the value of xxx_param is not set bcz file is missing")

    def test_3_key_error():
        '''
        specified value with key does not found
        '''
        print(' -- usecase3_error: set load key which does not exist in the dict')
        config = KissConfig()
        # the 1st (lowest) layer
        config.append(dict(configfile='a_missing_file.yml'))
        config.append(ConfigFile(key='configfile_bad_key', required=False))
        try:
            value = config.commit()
        except FileNotFoundError:
            log.debug("expected FileNotFoundError")
        try:
            pprint("{} {}".format('xxx_param', config['xxx_param']))
        except KeyError:
            log.debug("the value of xxx_param is not set bcz file is missing")

    def test_4():
        print(' --  usecase4 accessing config value as an attribute after callinig the commit method.')
        config = KissConfig()
        # the 1st (lowest) layer
        config.append(dict(verbose=False))
        config.append(dict(xxx_param=3.1415926))
        # the 2nd layer (for a hard coded arguments)
        parser = ArgumentParser()
        parser.add_argument("-v", "--verbose", action='store_true')
        args = parser.parse_args(['--verbose']) # hard coded arguments
        config.append(args)
        config.commit()
        # accessing as an attribute.
        print("verbose = {}".format(config.verbose))
        print("xxx = {}".format(config.xxx_param))

    def test_5():
        '''
        layer1:  dict(Architecture='{{HOSTNAME}}')         # 書式を先に
        layer2:  {'HOSTNAME': 'HogeNoteBook'}              # 変数を後に Extract(辞書) で投入.

        in use
        {'Architecture': 'HogeNoteBook'}                   # 

        '''
        print(' -- usecase5 extraction')
        config = KissConfig()

        # no 1 layer
        config.append(dict(Architecture='{{HOSTNAME}}'))
        # no 2 layer
        config.append(Extract(dict(HOSTNAME='HogeNoteBook')))
        value = config.commit()
        print(value.summary())

    def test_6():
        '''
        置き換えられない例.

        layer1:  dict(Architecture='{{HOSTNAME}}', Architecture2='{{HOSTNAME}}_ABCD') # 書式を先に
        layer2:  extract --- {'HOSTNAME': 'HogeNoteBook'}                             # 変数を後に Extract(辞書) で投入.
        layer3:  dict(Architecture3='{{HOSTNAME}}'                                    # こちらはスルーされる.

        -- usecase6 extraction
        {'Architecture': 'HogeNoteBook',
        'Architecture2': 'HogeNoteBook_ABCD',
        'Architecture3': '{{HOSTNAME}}'}  <-- a higher layer is not replaced with a lower Extrace

        '''
        print(' -- usecase6 extraction')
        config = KissConfig()
        # no 1 layer
        config.append(
            dict(Architecture='{{HOSTNAME}}', Architecture2='{{HOSTNAME}}_ABCD'))
        # no 2 layer
        config.append(Extract(dict(HOSTNAME='HogeNoteBook')))
        # no 3 layer
        config.append(dict(Architecture3='{{HOSTNAME}}'))
        value = config.commit()
        print(value.summary())

    def test_7():
        print(' -- usecase7: copying to **kw')
        config = KissConfig()
        # the 1st (lowest) layer
        config.append(dict(abc=dict(defg='hijklmn')))
        config.commit()
        print('config.abc.defg {}'.format(config.abc.defg))

        def func(**kw):
            print("kw = {}".format(kw))
            print("kw['abc'] = {}".format(kw['abc']))
            print("kw['abc']['defg'] = {}".format(kw['abc']['defg']))

        func(**config)

        def func_obj(obj):
            print("obj = {}".format(obj))
            print("obj['abc'] = {}".format(obj['abc']))
            print("obj['abc']['defg'] = {}".format(obj['abc']['defg']))
            print("obj.abc = {}".format(obj.abc))
            print("obj.abc.defg = {}".format(obj.abc.defg))

        func_obj(config)

    def test_8(optional=True):
        print(' -- usecase8 optional file(not required)')
        config = KissConfig()
        config.append(ConfigFile('a_missing_file.yml', optional=optional))
        value = config.commit()
        pprint(value)

    def test_8_error(required=True):
        print(' -- usecase8_error required file does not exist')
        config = KissConfig()
        try:
            fn = 'a_missing_file.yml'
            config.append(ConfigFile(fn, required=required))
            value = config.commit()
            log.debug(
                'test_8_error after a missing file a_missing_file.yml processed')
        except FileNotFoundError as e:
            log.debug("expected FileNotFoundError {}".format(e))

    def test_9():
        print(' -- usecase9 ConfigFile with dest param')
        config = KissConfig()
        config.append(ConfigFile('test3.yml', dest='mytest3'))
        config.commit()
        pprint([k for k in config.keys()])
        pprint([(k, config['mytest3'][k]) for k in config['mytest3'].keys()])

    def test_10():
        print(' -- usecase10 environment valualbe integration')
        config = KissConfig()
        config.append(EnvValue(exclude='^T.*'))  # choose with regex
        #config.append(EnvValue())  # import all envvaluables
        config.commit()
        pprint([k for k in config.keys()])

    def main():
        log.basicConfig(level=log.DEBUG)
        test_0()
        test_1()
        test_2()
        test_2_a()
        test_3()
        test_3_error()
        test_3_key_error()
        test_4()
        test_5()
        test_6()
        test_7()
        test_8(True)
        try:
            test_8(False)
        except FileNotFoundError:
            log.info('expected FileNotFoundError')
            pass
        test_8_error(True)
        test_8_error(False)
        test_9()
        test_10()

    main()

"""

from kissconfig import KissConfig, ArgumentParser  #, ConfigFile

def test_1():
    """
    ベースのconfigがあってArgumentParserの値とミックスする.

    python3 examples.py -v  <--- こちらだと ArgumentParserの値が反映される.
    python3 examples.py     <--- こちらだと データの値が優先される.

    ArgumentParserのデフォルト値を設定は可能ではあるがデータ・ドリブンにし辛いところがあるがそこが解決される.

    """
    print(' -- usecase1: default layer and ArgumentParser layeer')
    config = KissConfig()
    # the 1st (lowest) layer
    config.append(dict(verbose=False))
    # the 2nd layer
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true')

    # ハードコードコマンドラインバージョン..
    # args = parser.parse_args(['--verbose'])
    args = parser.parse_args()
    config.append(args)
    value = config.commit()
    print(config.summary())

test_1()    
