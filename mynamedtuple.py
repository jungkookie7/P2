import keyword

def mynamedtuple(type_name, field_names, mutable=False, defaults={}):
    # testing type_name
    if type(type_name) != str:  # test if a string
        raise SyntaxError
    elif not type_name[0].isalpha():  # test if first element is letter
        raise SyntaxError
    elif keyword.iskeyword(type_name):  # test if conflicts with keywords
        raise SyntaxError
    else:  # passes all tests
        pass
    
    # testing field_names
    if type(field_names) == str:  # tests if str, if so splits
        field_names = field_names.replace(',', ' ').split()

    if type(field_names) != list or len(field_names) == 0:  # tests if field_name is NOT a list or empty
        raise SyntaxError

    for i in field_names:
        if not i[0].isalpha():  # tests if first element is letter
            raise SyntaxError
        elif keyword.iskeyword(i):  # tests if conflicts with keywords
            raise SyntaxError
        else:  # passes all tests
            pass

    # testing for duplicates
    a = []
    seen = {}  

    for name in field_names:
        if name not in seen:
            a.append(name)
            seen[name] = True  
    field_names = a

    # testing defaults
    if type(defaults) != dict:  # tests if default is a dict
        raise SyntaxError
    
    for i in defaults:
        if i not in field_names:  # tests if element is in field_name
            raise SyntaxError
        else:  # passes all tests
            pass
    
    # new line and tab
    new = ('\n')
    tab = ('    ')

    # class code
    big_string = (f'class {type_name}:')
    big_string += new
    big_string += (f'{tab}_fields = {field_names}')
    big_string += new
    big_string += (f'{tab}_mutable = {mutable}')
    big_string += new

    # __init__
    init_params = ''
    for name in field_names:
        init_params += f"{name}={defaults.get(name, 'None')}, "
    init_params = init_params.rstrip(', ')  
    big_string += f"{tab}def __init__(self, {init_params}):{new}"
    
    for name in field_names:
        big_string += f"{tab*2}self.{name} = {name}{new}"
    big_string += new

    # __repr__ method
    big_string += f"{tab}def __repr__(self):{new}"
    repr_fields = ''
    for name in field_names:
        repr_fields += f"{name}={{self.{name}!r}},"
    repr_fields = repr_fields.rstrip(', ')  
    big_string += f"{tab*2}return f'{type_name}({repr_fields})'{new}{new}"

    # Accessor methods
    for name in field_names:
        big_string += f"    def get_{name}(self):\n"
        big_string += f"        return self.{name}\n\n"

    # __getitem__ method
    big_string += "    def __getitem__(self, index):\n"
    big_string += f"        return getattr(self, self._fields[index])\n\n"

    # __eq__ method
    big_string += "    def __eq__(self, other):\n"
    big_string += "        if not isinstance(other, self.__class__):\n"
    big_string += "            return NotImplemented\n"
    big_string += "        return all(getattr(self, name) == getattr(other, name) for name in self._fields)\n\n"

    # asdict method
    big_string += "    def asdict(self):\n"
    big_string += "        return {name: getattr(self, name) for name in self._fields}\n\n"

    # asdict method
    big_string += "    def asdict(self):\n"
    big_string += "        return {name: getattr(self, name) for name in self._fields}\n\n"

    # make method
    big_string += "    @classmethod\n"
    big_string += "    def make(cls, iterable):\n"
    big_string += "        return cls(*iterable)\n\n"

    # _make method
    big_string += "    @classmethod\n"
    big_string += "    def _make(cls, iterable):\n"
    big_string += "        return cls(*iterable)\n\n"

    # replace method
    big_string += "    def replace(self, **kwargs):\n"
    big_string += "        if self._mutable:\n"
    big_string += "            for name, value in kwargs.items():\n"
    big_string += "                if name in self._fields:\n"
    big_string += "                    object.__setattr__(self, name, value)\n"
    big_string += "            return None\n"
    big_string += "        else:\n"
    big_string += "            new_values = {name: kwargs.get(name, getattr(self, name)) for name in self._fields}\n"
    big_string += "            return self.__class__(**new_values)\n\n"

    # _replace method
    big_string += "    def _replace(self, **kwargs):\n"
    big_string += "        new_values = {name: kwargs.get(name, getattr(self, name)) for name in self._fields}\n"
    big_string += "        return self.__class__(**new_values)\n\n"

    # __setattr__ method
    big_string += "    def __setattr__(self, name, value):\n"
    big_string += "        if self._mutable or name not in self._fields or not hasattr(self, name):\n"
    big_string += "            object.__setattr__(self, name, value)\n"
    big_string += "        else:\n"
    big_string += "            raise AttributeError(f'Cannot modify {name} in immutable {self.__class__.__name__}')\n"

    # Execute the generated class code
    namespace = {}
    exec(big_string, namespace)
    return namespace[type_name]

# TESTERS
coordinate = mynamedtuple('coordinate', ['x', 'y'], mutable=False)  # testing tuple number 1
p = coordinate(0, 0)
print(p)  # coordinate(x=0, y=0)
print(p.asdict())  # {'x': 0, 'y': 0}
