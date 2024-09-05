#coding:utf-8
import collections

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
        self.update(dict(*args, **kwargs))  # use the free update to set keys

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
                    child = objdict(child)
                    self.store[name] = child
                    return child
                elif isinstance(child, list) and not isinstance(child, objdict):
                    pass
                else:
                    return child
            else:
                return object.__getattr__(self, name)
        except AttributeError as e:
            raise e       


if __name__ == '__main__':

    xx = objdict()

    xx['key'] = 123
    xx['my'] = dict(child=dict(grand_child='the grand child'))

    print("Repr xx:{}".format(xx))
    print("xx.key: <{}>".format(xx.key))
    print("xx.my.child.grand_child: <{}>".format(xx.my.child.grand_child))
