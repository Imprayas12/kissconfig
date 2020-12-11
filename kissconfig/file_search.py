""" a utility to find a file from some attributes.  (alhpa version)

def file_search(name_pattern_list, path_list=['.']):


* usecases

- open a file according to the determined priority.
  - alert all files to the user that match condition. 
- open all files according to the search condition.

@todo regular expression mode.

  name_pattern_list
  path_list

find files from multi layered searching pattern

/hoge/fuga/piyo.json
/hoge/fuga.bak/piyo.json
/hoge.bak/fuga/piyo.json


@todo 複数のファイルがみつかりました warning 


"""

import os
import re
import platform
from glob import glob

path_name_must_end_with_a_separator = True

def file_search(name_pattern_list=['*.conf'], path_list=['.']):
    """
    input:
       name_pattern_list 
       path_list
    returns:
       existing file lists

    usecase 1:
       - path_list
       - name_pattern
    """
    if isinstance(name_pattern_list, str):
        name_pattern_list = [name_pattern_list]
    elif not isinstance(name_pattern_list, list):
        assert False, "a str or a list is accepted instead of the {}".format(type(name_pattern_list))
    org_alt_li = _macro_extract(path_list)
    ar = []
    for path_org_alt in org_alt_li:
        path_org_alt = list(path_org_alt[:]) #shallow copy
        if path_name_must_end_with_a_separator:
            if not (path_org_alt[-1] == os.sep or path_org_alt[-1] != '.'):
                raise RuntimeError("add separator at end of the path name {}".format(path_org_alt))
        for name_pattern in name_pattern_list:
            path_n, file_n = os.path.split(name_pattern)
            if path_n != '':
                pn = name_pattern
            else:
                pn = os.path.join(_separator_norm(path_org_alt[1]), name_pattern)
            if _like_glob(pn):
                epn = _glob_ext(pn)
                if isinstance(epn, list) and len(epn) and os.path.exists(epn[0]):
                    ar.append(epn[0])
            else:
                if os.path.exists(pn):
                    ar.append(pn)
                else:
                    pass
    return ar
                
def _separator_norm(name):
    if 'Win' in platform.system():
        replaced = name.replace("/", os.sep)
    else:
        replaced = name.replace("\\", os.sep)
    return replaced

def _macro_extract(contents):
    """
    '~': user folder or LocalAppData on win

    returns:
        [(org, altered),...]

    >>> _macro_extract(["{HOME}/aaa"])

    >>> _macro_extract(["~/aaa"])
    """
    alt = []
    for item in contents:
        item2 = os.path.expanduser(item)
        alt.append((item, item2))
    return alt

def _like_glob(item):
    if '*'  in item:
        return True
    #if '.'  in item:
    #    return True

def _glob_ext(item):
    return glob(item)


__all__ = ['file_search']

if __name__ == '__main__':
    def test_case1():
        print("test_case1")
        y = file_search('gdb', path_list=["/usr/local/share/", "/usr/share/"])
        print(y)

    def test_case2():
        # use case system wide file and user file.
        print("test_case2")
        pn1 = "/tmp/abc/def/"
        pn2 = "/tmp/abc/geh/"
        if not os.path.exists(pn1):
            os.makedirs(pn1)
        if not os.path.exists(pn2):
            os.makedirs(pn2)
        open(os.path.join(pn1, ".hoge.conf"), "w").write("test1_user")
        open(os.path.join(pn2, "hoge.conf"), "w").write("test1_system_wide")
        y = file_search([".hoge.conf", "hoge.conf"], path_list=[pn1, pn2])
        print(y)

    def test_case3():
        print("test_case3")
        y = file_search(name_pattern_list=['*.conf'], path_list=['.'])
        print(y)
        
    test_case1()
    test_case2()
    test_case3()


    
