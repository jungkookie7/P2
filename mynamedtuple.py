import keyword

def mynamedtuple(type_name, field_names, mutable=False, defaults={}):
    # testing type_name
    if type(type_name) != str: 
        raise SyntaxError
    elif not type_name[0].isalpha():  
        raise SyntaxError
    elif keyword.iskeyword(type_name):  
        raise SyntaxError
    else:  
        pass
    
    # testing field_names
    if type(field_names) == str: 
        field_names = field_names.replace(',', ' ').split()

    if type(field_names) != list or len(field_names) == 0:  
        raise SyntaxError

    for i in field_names:
        if not i[0].isalpha():  
            raise SyntaxError
        elif keyword.iskeyword(i):  
            raise SyntaxError
        else:  
            pass

    # testing for duplicates
    lst = []
    seen = {}  

    for i in field_names:
        if i not in seen:
            lst.append(i)
            seen[i] = True  
    field_names = lst

    # testing defaults
    if type(defaults) != dict:  
        raise SyntaxError
    
    for i in defaults:
        if i not in field_names:  
            raise SyntaxError
        else: 
            pass
    
    # new line and tab
    new = ('\n')
    tab = ('    ')

    #large freaking gawd damn string
    big_string = (f'class {type_name}:')
    big_string += new
    big_string += (f'{tab}_fields = {field_names}')
    big_string += new
    big_string += (f'{tab}_mutable = {mutable}')
    big_string += new
    #print(big_string) *TEST MIDWAY

    # __init__
    init_params = ''
    for name in field_names:
        init_params += f"{name}={defaults.get(name, 'None')}, "
    init_params = init_params.rstrip(', ')  
    big_string += f"{tab}def __init__(self, {init_params}):{new}"
    
    for name in field_names:
        big_string += f"{tab*2}self.{name} = {name}{new}"
    big_string += new
    #print(big_string) *TEST MIDWAY

    # __repr__ 
    big_string += f"{tab}def __repr__(self):{new}"
    repr_fields = ''
    for name in field_names:
        repr_fields += f"{name}={{self.{name}!r}},"
    repr_fields = repr_fields.rstrip(', ')  
    big_string += f"{tab*2}return f'{type_name}({repr_fields})'{new*2}"
    #print(big_string) *TEST MIDWAY

    # query/accesors 
    for name in field_names:
        big_string += (f'{tab}def get_{name}(self):{new}')
        big_string += (f'{tab*2}return self.{name}{new*2}')
    #print(big_string) *TEST MIDWAY

    # __getitem__ 
    big_string += (f'{tab}def __getitem__(self, index):{new}')
    big_string += (f'{tab*2}return getattr(self, self._fields[index]){new*2}')
    #print(big_string) *TEST MIDWAY

    # __eq__ 
    big_string += (f'{tab}def __eq__(self, other):{new}')
    big_string += (f'{tab*2}if not isinstance(other, self.__class__):{new}')
    big_string += (f'{tab*3}return NotImplemented{new}')
    big_string += (f'{tab*2}return all(getattr(self, name) == getattr(other, name) for name in self._fields){new}')
    #print(big_string) *TEST MIDWAY

    # asdict 
    big_string += (f'{tab}def _asdict(self):{new}')
    big_string += (f"{tab*2}return {{name: getattr(self, name) for name in self._fields}}{new*2}")
    #print(big_string) *TEST MIDWAY

    # make 
    big_string += (f'{tab}@classmethod{new}')
    big_string += (f'{tab}def make(cls, iterable):{new}')
    big_string += (f'{tab*2}return cls(*iterable){new*2}')
    #print(big_string) *TEST MIDWAY

    # _make 
    big_string += (f'{tab}@classmethod{new}')
    big_string += (f'{tab}def _make(cls, iterable):{new}')
    big_string += (f'{tab*2}return cls(*iterable){new*2}')
    #print(big_string) *TEST MIDWAY

    # replace 
    big_string += (f'{tab}def replace(self, **kwargs):{new}')
    big_string += (f'{tab*2}if self._mutable:{new}')
    big_string += (f'{tab*3}for name, value in kwargs.items():{new}')
    big_string += (f'{tab*4}if name in self._fields:{new}')
    big_string += (f'{tab*5}object.__setattr__(self, name, value){new}')
    big_string += (f'{tab*3}return {None}{new}')
    print(big_string) 
    #WHY IS IT NOT WORKING

    # _replace 
    big_string += (f'{tab}def _replace(self, **kwargs):{new}')
    big_string += '        new_values = {name: kwargs.get(name, getattr(self, name)) for name in self._fields}\n'
    big_string += (f'{tab*2}return self.__class__(**new_values){new*2}')
    #print(big_string) *TEST MIDWAY

    # __setattr__ 
    big_string += (f'{tab}def __setattr__(self, name, value):{new}')
    big_string += (f'{tab*2}if self._mutable or name not in self._fields or not hasattr(self, name):{new}')
    big_string += (f'{tab*3}object.__setattr__(self, name, value){new}')
    big_string += (f'{tab*2}else:{new}')
    big_string += (f'{tab*3}raise AttributeError{new}')
    #print(big_string) *TEST MIDWAY

    # exec
    namespace = {}
    exec(big_string, namespace)
    return namespace[type_name]
