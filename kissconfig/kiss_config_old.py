# coding:utf-8
""" kiss_config.py

simple stupid configuration 
author: taka@opus.co.jp
python version: above Python3.3
"""

"""
基本な感じ

* 実際configには階層がある

 - グローバル静的
 - ローカル静的
 - ローカル動的

* 特別な感じ

 - Extract で 文字列変数解決 ... $(hoge) を fuga に変えるようなこと.
 - ConfigLoad ファイル名読み込み
 - ConfigLoad 変数ファイル名読み込み

@TODO: ドキュメントは日本語で書いてから英語にかえればよいとおもいます
@TODO: document ConfigFile(x, required=True)
@TODO: document ConfigFile(key=x, required=True)
@TODO: Read command which just loads file not parse
@TODO: 対話的にコード生成とかできたらいいんじゃないですかね??  それか、テンプレートを出力してくれるようにするとか??

@done: Loadという一般的すぎる名前 import * で良くない. LoadでなくてConfigFile にした.
@done: argparse を内包しているから 同名でつかえるようにしてほしい. (import行がへる)
@done: commit前に後レイヤーから前レイヤーにアクセスしたい.
@done: Environmental Valualble integration. (choose regex, exclude regex), mangling character name.

- 典型的な使い方例1
  3層の設定、下に行くほど派生的に優先度高い.
  - static_config.yml
  - defaultで prod.yml
  - 指定で dev.yml

"""
# standard modules.
import os
import sys
import argparse
import collections
from pprint import pprint, pformat

import logging as log

# pip
import yaml

import re

BEGIN_TOKEN = '{{'
END_TOKEN = '}}'
REXP = r'({0}\s*(?P<word>.*?)\s*{1})'.format(BEGIN_TOKEN, END_TOKEN)
REX = re.compile(REXP)
LEAVE_NOT_FOUND = True
LOAD_REQUIRED_DEFAULT = False

def embedded_value_extraction(text, data, **kw):
    """ extract formatted text with dict,
        format is like {{key}}

    :text: text_format 
    :data: dict
    :**kw: leave_not_found==True leave {{value}} format string as is 
           when the value is not in the dict

    >>> data = dict(name="Taro", de="doing", ge="today.", hi="good", lm="bye!")
    >>> text = "hello {{    name    }}, how are you {{de}} {{ ge }} bye {{hi }}{{ lm}}"
    >>> embedded_value_extraction(text, data)
    'hello Taro, how are you doing today. bye goodbye!'

    >>> data = dict()
    >>> text = "hello {{missing}}"
    >>> embedded_value_extraction(text, data, leave_not_found=False)
    'hello '

    >>> data = dict(name="Taro", lm="bye!")
    >>> text = "bye {{missing}}EEEE"
    >>> embedded_value_extraction(text, data, leave_not_found=True)
    'bye {{missing}}EEEE'

    """
    leave_not_found = kw.get('leave_not_found', LEAVE_NOT_FOUND)
    buf = ''
    pos = 0
    for idx, m in enumerate(REX.finditer(text)):
        match_phrase = m.group(0)
        key = m.group('word')
        buf += text[pos:m.start()]
        if key in data:
            buf += data[key]
        else:
            if leave_not_found:
                buf += match_phrase
        pos = m.end()
    buf += text[pos:]
    return buf


def extractValue(subject_dict, modifier_dict):
    """ string formatted "{{VALUE}}" value extraction.

    :subject_dict: a dict may include formatted string value 
    :modifier_dict: a dict have value_name and value_replacing pairs.

    ex)
    subject_dict example
       dict(keyx="{{USERNAME}}") 
    modifier_dict_dict example
       dict(USERNAME="Alice") 
    result
       dict(keyx="Alice") 

    """
    for key in subject_dict:
        subject = subject_dict[key]
        if isinstance(subject, str):
            modified = embedded_value_extraction(subject, modifier_dict)
            if subject_dict[key] != modified:
                subject_dict[key] = modified
    return subject_dict

class EnvValue(object):
    """
    :keywords: 

    :choose: regex      
    :exclude: regex     

    >>> import os
    >>> import re
    >>> env = EnvValue(choose="^T", exclude="^TMP")
    >>> print(env.data)
    """
    #     >>> [k for k in os.environ]
    def __init__(self, **kw):
        self.data = {k: os.environ[k] for k in os.environ}
        if not 'choose' in kw:
            kw['choose'] = '.*' # all
        chooserex = re.compile(kw.get('choose'))
        self.data = {k: self.data[k] for k in self.data if chooserex.match(k)}
        if 'exclude' in kw:
            excluderex = re.compile(kw.get('exclude'))
            self.data = {k: self.data[k] for k in self.data if not excluderex.match(k)}

    def _commit(self, idx, tree):
        return self.data
            
class ConfigFile(object):
    """ loading a indirect config file.

    :ar[0]:    specify file_name to load (optional)

    :keywords: 

    :key:      a pointer of a dict key for the filename
    :optional:  true when thru on missing file
    :required:  true when error on missing file
    :dest:     loaded dict will be associated dict[dest] if `dest` is specified.

    @WIP Ignore missing file
    """

    def __init__(self, *ar, **kw):
        """

        :*ar:  specify a file by a ar[0]
        :**kw: specify a keyword which points to a filename of the total layer dict.

        """
        self.name = None
        self.dest = kw.get('dest')
        self.required = kw.get('required', LOAD_REQUIRED_DEFAULT)
        self.key = kw.get('key')
        if len(ar) > 0 and isinstance(ar[0], str):
            self.name = ar[0]
            if not os.path.exists(self.name) and self.required == True:
                raise FileNotFoundError(
                    "specified indirect file {} is not found".format(self.name))

    def _commit(self, idx, kconfig):
        """ 

        :kconfig: dict for self.key
        :return:  if None object must be skipped to process.
        """
        key_not_found = True
        if self.key:
            log.debug("ConfigFile {}".format(self.key))
            # indirect filename mode
            if callable(self.key):
                self.name = self.key(kconfig)
            elif self.key in kconfig:
                # 普通に下請けの確定はよばれる、しかし key参照するために kconfig.get のなかで、db参照がある、dbを確定させないといけない ?? (そっか...)
                key_not_found = False
                self.name = kconfig.get(self.key, limit_layer=idx)
                if self.name == None:
                    log.debug(
                        "{} is not specified in the dict".format(self.key))
                    if self.required == False:
                        return None
                    else:
                        raise RuntimeError(
                            "file specified key {} is not found".format(self.key))
            else:
                key_not_found = True
            if self.required == True:
                RuntimeError("with the specified key \'{}\', the value is not found. {}".format(
                    self.key, kconfig))

        if self.required:
            if self.name is None:
                if key_not_found is True:
                    raise RuntimeError(
                        "not found the value associated by the key `{}` specified".format(self.key))
                raise RuntimeError("a name parameter not specified")
        else:
            # not self.required:
            if self.name is None and key_not_found:
                return None

        if not isinstance(self.name, str):
            raise RuntimeError(
                "expected str type for a file name {}".format(self.name))
        try:
            with open(self.name, 'r') as f:
                self.value = yaml.load(f, yaml.SafeLoader)
                assert isinstance(self.value, dict)  # requisites: top level type must be dict for loading data
            return extractValue(self.value, kconfig)
        except FileNotFoundError as e:
            if self.required:
                raise FileNotFoundError(
                    "the specified indirect file {} error:{}".format(self.name, e))
            else:
                log.debug(
                    "the specified file name {} does not exist and ConfigFile argument set optional".format(self.name))
        except Exception as e:
            raise e

class Load(ConfigFile):
    """ this class name is not good for public. it has been replaced with ConfigFile.
    """
    def __init__(self, *ar, **kw):
        import warnings
        warnings.warn("`Load` is deprecated and will be removed in future, use `ConfigFile` instead")
        super(Load, self).__init__(*ar, **kw)


class Extract():
    def __init__(self, extract_dict, **kw):
        """ replace main dict with the dict(key, value)

        """
        self.extract_dict = extract_dict

    def _commit(self, idx, tree):
        """ 既存の親定義について、extract value する. """
        for k in tree:
            ary = tree[k]
            for idx, x in enumerate(ary):
                val = x['value']
                y = embedded_value_extraction(val, self.extract_dict)
                if val != y:
                    x['value'] = y

class objdict(collections.abc.MutableMapping):
    """A dictionary can be accessed by attr.

    >> xx = objdict()
    >> xx['key'] = 123
    >> xx.key
    123
    >> xx['key1'] = dict(key2='grand child')
    >> xx.key1.key2
    grand child

    """
    def __init__(self, *args, **kwargs):
        self.store = dict()
        try:
            self.update(dict(*args, **kwargs))  # use the free update to set keys
        except:
            import pdb; pdb.set_trace()

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    def __getattr__(self, name):
        try:
            if name in self.store:
                child = self.store[name]
                if isinstance(child, dict) and not isinstance(child, objdict):
                    # replace child dict as `objdict`
                    child = objdict(child)
                    self.store[name] = child
                    return child
                else:
                    return child
            raise AttributeError('{} not found'.format(name))
        except AttributeError as e:
            raise e

class KissConfig(objdict):

    def __init__(self):
        """ 
        no arguments
        """
        self.commit_level = None
        super(KissConfig, self).__init__()
        self._ary = []
        self.commited = False

    def append(self, layer):
        """ append a layer.

        :layer: dict, ConfigFile, Extract object
        """
        self._ary.append(layer)

    def insert(self, pos, layer):
        """ insert a layer.

        :pos: same as postiont of list.insert
        :layer: dict, ConfigFile, Extract object
        """
        self._ary.insert(pos, layer)

    def get(self, key, limit_layer=None, default=None):
        """ dynamic search from self._tree. 

        :key: dict key
        return None or specified default value at kwargs 
        if the associated item could not be found
        """
        """
        ここの分岐のユースケース.  (間違えてcommitしている以外でgetしてきたら親切的にcommitしてから返答する)
        だからcommit_levelが Noneであることが前提. 
        """
        if self.commit_level is None: #
            if not self.commited:
                self.commit()  # ここでルーブ

        if key in self._tree:
            return self._tree[key][-1]['value']
        else:
            return default

    def commit(self):
        """ setup after the all layers have been appended.

        """
        self._tree = dict()
        for idx, item in enumerate(self._ary):
            self.commit_level = idx
            if isinstance(item, ConfigFile):
                _itm = item._commit(idx, self) ## <--- bug
                if _itm == None:
                    continue
                if item.dest != None:
                    dest_ky = item.dest
                    item = {dest_ky: {k: _itm[k] for k in _itm}}
                else:
                    item = _itm
            elif isinstance(item, EnvValue):
                item = item._commit(idx, self)
            elif isinstance(item, Extract):
                item._commit(idx, self._tree)
                continue
            elif isinstance(item, argparse.Namespace):
                item = {it[0]: it[1] for it in item._get_kwargs()}
            elif isinstance(item, dict):
                pass
            else:
                raise RuntimeError('unknown type data {}'.format(repr(item)))
            assert item != None
            # storing layered key-value buffer
            for ky in item:
                if not ky in self._tree:
                    self._tree[ky] = []
                self._tree[ky].append(dict(idx=idx, value=item[ky]))

        for idx, ky in enumerate(self._tree):
            self[ky] = self._tree[ky][-1]['value']
        self.commited = True
        return self

    def __contains__(self, item):
        return item in self._tree

    def __repr__(self):
        return "<{} at 0x{:x}>".format(type(self).__name__, id(self))

    def summary(self, **kw):
        """ @WIP return string of data structure by yaml format """
        import yaml
        return "{}\n{}".format(str(self.__class__),
                               yaml.dump([[k, self.store[k]]
                                          for k in self.store], default_flow_style=False)
                               )

# wrapper of ArgumentParser
from argparse import ArgumentParser

__all__ = ('KissConfig', 'Load', 'ConfigFile', 'Extract', 'ArgumentParser', 'EnvValue')


