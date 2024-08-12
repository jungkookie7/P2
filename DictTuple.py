from mynamedtuple import mynamedtuple

class DictTuple:
    def __init__(self, *args):
        self.dt = []

        if len(args) == 0:
            raise AssertionError('cannot be empty')
        for i in args:
            if type(i) != dict:
                raise AssertionError('not a dict')
            if not i:
                raise AssertionError
            self.dt.append(i)

    def __len__(self):
        keys = 0  
        empty_list = []  
        for i in self.dt:
            for key in i.keys():
                if key not in empty_list:  
                    empty_list.append(key)  
                    keys += 1  
        return keys  

    def __bool__(self):
        if len(self.dt) == 1:
            return False
        else:
            return True

    def __repr__(self):
        another_list = []
        for i in self.dt:
            string_version = repr(i)
            another_list.append(string_version)
        together = ', '.join(another_list)
        return (f'DictTuple({together})')

    def __contains__(self, key):
        for i in self.dt:
            if key in i:
                return True
        return False

    def __getitem__(self, key):
        reversed_dicts = reversed(self.dt)
        for i in reversed_dicts:
            if key in i:
                return i[key]
        raise KeyError('key is in no dictionaries in list')

    def __setitem__(self, key, value):
        reversed_dicts = reversed(self.dt)
        for i in reversed_dicts:
            if key in i:
                i[key] = value
                return
        self.dt.append({key: value})

    def __delitem__(self, key):
        deleted = False
        for i in self.dt:   
            if key in i:
                del i[key]
                deleted = True
        if deleted == False:
            raise KeyError

    def __call__(self, key):
        another_freaking_list = []
        for i in self.dt:
            if key in i:
                another_freaking_list.append(i[key])
        return another_freaking_list

    def __iter__(self):
        lst = []
        reversed_dicts = reversed(self.dt)
        for i in reversed_dicts:
            sorted_values = sorted(i)
            for a in sorted_values:
                if a not in lst:
                    lst.append(a)
        return iter(lst)

    def __eq__(self, other):
        len_self = len(self)
        len_other = len(other)  
        if type(other) == DictTuple:
            if len_self == len_other:
                for key in self:
                    if self[key] == other[key]:
                        pass
                    elif self[key] != other[key]:
                        return False
            elif len_self != len_other:
                    return False
            return True
        elif type(other) == dict:
            if len_self == len_other:
                for key in self:
                    if self[key] == other.get(key):
                        pass
                    elif self[key] != other.get(key):
                        return False
            elif len_self != len_other:
                return False
            return True
        return False
    
    def __add__(self, other):
        if type(other) == DictTuple:
            new_new_list = []
            for i in (*self.dt, *other.dt):
                if len(i) != 0:
                    new_new_list.append(i)  
            return DictTuple(*new_new_list)

        if type(other) == dict:
            if len(other) != 0:  
                return DictTuple(*self.dt, other)
            else:
                raise AssertionError       
        else:
            raise TypeError('not DictTuple or dict')

    def __setattr__(self, name, value):
        if name == "dt":
            self.__dict__[name] = value
        else:
            raise AssertionError('cannot add new attributes to object')

#TESTERS
coordinate = mynamedtuple('coordinate', 'x y')
d = DictTuple({'c1': coordinate(1, 2)}, {'c1': coordinate(3, 4)})
print(d)
