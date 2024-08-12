import keyword

def mynamedtuple(type_name, field_names, mutable=False, defaults={}):
    # testing type_name
    if type(type_name) != str: 
        raise SyntaxError
    elif not type_name[0].isalpha():  
        raise SyntaxError
    elif keyword.iskeyword(type_name):  
        raise SyntaxError
    
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
    
    # new line and tab
    new = '\n'
    tab = '    '

    # large string for the class
    big_string = f'class {type_name}:'
    big_string += new
    big_string += f'{tab}_fields = {field_names}'
    big_string += new
    big_string += f'{tab}_mutable = {mutable}'
    big_string += new

    # __init__
    init_params = ', '.join(f"{name}={defaults.get(name, 'None')}" for name in field_names)
    big_string += f"{tab}def __init__(self, {init_params}):{new}"
    
    for name in field_names:
        big_string += f"{tab*2}self.{name} = {name}{new}"
    big_string += new

    # __repr__ method
    big_string += f"{tab}def __repr__(self):{new}"
    repr_fields = ', '.join(f"{name}={{self.{name}!r}}" for name in field_names)
    big_string += f"{tab*2}return f'{type_name}({repr_fields})'{new}{new}"

    # Accessor methods
    for name in field_names:
        big_string += f"{tab}def get_{name}(self):{new}"
        big_string += f"{tab*2}return self.{name}{new}{new}"

    # __getitem__ method
    big_string += f"{tab}def __getitem__(self, index):{new}"
    big_string += f"{tab*2}return getattr(self, self._fields[index]){new}{new}"

    # __eq__ method
    big_string += f"{tab}def __eq__(self, other):{new}"
    big_string += f"{tab*2}if not isinstance(other, self.__class__):{new}"
    big_string += f"{tab*3}return NotImplemented{new}"
    big_string += f"{tab*2}return all(getattr(self, name) == getattr(other, name) for name in self._fields){new}{new}"

    # asdict method
    big_string += f"{tab}def asdict(self):{new}"
    big_string += f"{tab*2}return {{name: getattr(self, name) for name in self._fields}}{new}{new}"

    # make method
    big_string += f"{tab}@classmethod{new}"
    big_string += f"{tab}def make(cls, iterable):{new}"
    big_string += f"{tab*2}return cls(*iterable){new}{new}"

    # _make method
    big_string += f"{tab}@classmethod{new}"
    big_string += f"{tab}def _make(cls, iterable):{new}"
    big_string += f"{tab*2}return cls(*iterable){new}{new}"

    # replace method
    big_string += f"{tab}def replace(self, **kwargs):{new}"
    big_string += f"{tab*2}if self._mutable:{new}"
    big_string += f"{tab*3}for name, value in kwargs.items():{new}"
    big_string += f"{tab*4}if name in self._fields:{new}"
    big_string += f"{tab*5}object.__setattr__(self, name, value){new}"
    big_string += f"{tab*2}return None{new}"
    big_string += f"{tab*2}else:{new}"
    big_string += f"{tab*3}new_values = {{name: kwargs.get(name, getattr(self, name)) for name in self._fields}}{new}"
    big_string += f"{tab*3}return self.__class__(**new_values){new}{new}"

    # _replace method
    big_string += f"{tab}def _replace(self, **kwargs):{new}"
    big_string += f"{tab*2}new_values = {{name: kwargs.get(name, getattr(self, name)) for name in self._fields}}{new}"
    big_string += f"{tab*2}return self.__class__(**new_values){new}{new}"

    # __setattr__ method
    big_string += f"{tab}def __setattr__(self, name, value):{new}"
    big_string += f"{tab*2}if self._mutable or name not in self._fields or not hasattr(self, name):{new}"
    big_string += f"{tab*3}object.__setattr__(self, name, value){new}"
    big_string += f"{tab*2}else:{new}"
    big_string += f"{tab*3}raise AttributeError(f'Cannot modify {{name}} in immutable {{self.__class__.__name__}}'){new}"

    # Execute the generated class code
    namespace = {}
    exec(big_string, namespace)
    return namespace[type_name]

# TESTERS
coordinate = mynamedtuple('coordinate', ['x', 'y'], mutable=False)  # testing tuple number 1
p = coordinate(0, 0)
print(p)  # coordinate(x=0, y=0)
print(p.asdict())  # {'x': 0, 'y': 0}
