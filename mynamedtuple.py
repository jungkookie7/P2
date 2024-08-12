import keyword

def mynamedtuple(type_name, field_names, mutable=False, defaults={}):
    # Validate type_name
    if not isinstance(type_name, str):  # Test if a string
        raise SyntaxError("Type name must be a string")
    if not type_name[0].isalpha():  # Test if first element is letter 
        raise SyntaxError("Type name must start with a letter")
    if keyword.iskeyword(type_name):  # Test if conflicts with keywords
        raise SyntaxError("Type name cannot be a keyword")

    # Validate field_names
    if isinstance(field_names, str):  # Tests if str, if so splits
        field_names = field_names.replace(',', ' ').split()

    if not isinstance(field_names, list) or not field_names:  # Tests if field_name is NOT a list or empty
        raise SyntaxError("Field names must be a non-empty list")

    for name in field_names:
        if not name[0].isalpha():  # Tests if first element is letter
            raise SyntaxError(f"Field name '{name}' must start with a letter")
        if keyword.iskeyword(name):  # Tests if conflicts with keywords
            raise SyntaxError(f"Field name '{name}' cannot be a keyword")

    # Remove duplicates
    field_names = list(dict.fromkeys(field_names))  # Preserves order and removes duplicates

    # Validate defaults
    if not isinstance(defaults, dict):  # Tests if defaults is a dict
        raise SyntaxError("Defaults must be a dictionary")
    
    for key in defaults:
        if key not in field_names:  # Tests if element is in field_name
            raise SyntaxError(f"Default value for '{key}' not in field names")

    # Prepare class code
    new = '\n'
    tab = '    '

    class_code = f'class {type_name}:{new}'
    class_code += f'{tab}_fields = {field_names}{new}'
    class_code += f'{tab}_mutable = {mutable}{new}'

    # __init__ method
    init_params = ', '.join(f"{name}={defaults.get(name, 'None')}" for name in field_names)
    class_code += f"{tab}def __init__(self, {init_params}):{new}"
    for name in field_names:
        class_code += f"{tab*2}self.{name} = {name}{new}"
    class_code += new

    # __repr__ method
    class_code += f"{tab}def __repr__(self):{new}"
    repr_fields = ','.join(f"{name}={{self.{name}!r}}" for name in field_names)  # No space after comma
    class_code += f"{tab*2}return f'{type_name}({repr_fields})'{new}{new}"

    # Accessor methods
    for name in field_names:
        class_code += f"{tab}def get_{name}(self):{new}"
        class_code += f"{tab*2}return self.{name}{new}{new}"

    # __getitem__ method
    class_code += f"{tab}def __getitem__(self, index):{new}"
    class_code += f"{tab*2}return getattr(self, self._fields[index]){new}{new}"

    # __eq__ method
    class_code += f"{tab}def __eq__(self, other):{new}"
    class_code += f"{tab*2}if not isinstance(other, self.__class__):{new}"
    class_code += f"{tab*3}return NotImplemented{new}"
    class_code += f"{tab*2}return all(getattr(self, name) == getattr(other, name) for name in self._fields){new}{new}"

    # asdict method
    class_code += f"{tab}def asdict(self):{new}"
    class_code += f"{tab*2}return {{name: getattr(self, name) for name in self._fields}}{new}{new}"

    # make method
    class_code += f"{tab}@classmethod{new}"
    class_code += f"{tab}def make(cls, iterable):{new}"
    class_code += f"{tab*2}return cls(*iterable){new}{new}"

    # replace method
    class_code += f"{tab}def replace(self, **kwargs):{new}"
    class_code += f"{tab*2}if self._mutable:{new}"
    class_code += f"{tab*3}for name, value in kwargs.items():{new}"
    class_code += f"{tab*4}setattr(self, name, value){new}"
    class_code += f"{tab*3}return None{new}"
    class_code += f"{tab*2}else:{new}"
    class_code += f"{tab*3}new_values = {{name: kwargs.get(name, getattr(self, name)) for name in self._fields}}{new}"
    class_code += f"{tab*3}return self.__class__(**new_values){new}{new}"

    # __setattr__ method
    class_code += f"{tab}def __setattr__(self, name, value):{new}"
    class_code += f"{tab*2}if not self._mutable and name in self._fields and hasattr(self, name):{new}"
    class_code += f"{tab*3}raise AttributeError(f'Cannot modify {name} in immutable {self.__class__.__name__}'){new}"
    class_code += f"{tab*2}super().__setattr__(name, value){new}"

    # Execute the generated class code
    namespace = {}
    exec(class_code, namespace)
    return namespace[type_name]

# TESTERS
coordinate = mynamedtuple('coordinate', ['x', 'y'], mutable=False)
p = coordinate(0, 0)
print(p)  # coordinate(x=0, y=0)
print(p.asdict())  # {'x': 0, 'y': 0}
