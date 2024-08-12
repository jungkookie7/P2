import keyword

def mynamedtuple(type_name, field_names, mutable=False, defaults={}):
    #testing type_name
    if type(type_name) != str: #test if a string
        raise SyntaxError
    elif not type_name[0].isalpha(): #test if first element is letter 
        raise SyntaxError
    elif keyword.iskeyword(type_name): #test if conflicts with keywords
        raise SyntaxError
    else: #passes all tests
        pass
    
    #testing field_names
    if type(field_names) == str: #tests if str, if so splits
        field_names = field_names.replace(',', ' ').split()

    if type(field_names) != list or len(field_names) == 0: #tests if field_name is NOT a list or a empty
        raise SyntaxError

    for i in field_names:
        if not field_names[0].isalpha(): #tests if first element is letter
            raise SyntaxError
        elif keyword.iskeyword(i): #tests if conflicts with keywords
            raise SyntaxError
        else: #passes all tests
            pass

    #testing for duplicates
    empty_list = []
    seen = {}  

    for i in field_names:
        if i not in seen:
            empty_list.append(i)
            seen[i] = True  
    field_names = empty_list

    #testing defaults
    if type(defaults) != dict: #tests if default is a str
        raise SyntaxError
    
    for i in defaults:
        if i not in field_names: #tests if element is in field_name
            raise SyntaxError
        else: #passes all tests
            pass

    #TAB AND NEWLINE
    tab = ('\t')
    new = ('\n')

    #large_string header
    large_string = (f'{type_name}:')
    large_string += new
    large_string += (f'{tab}_fields = {field_names}')
    large_string += new
    large_string += (f'{tab}_mutable = {mutable}')
    large_string += new
    large_string += new

    # __init__ method
    init_params = []
    for name in field_names:
        default_value = defaults.get(name, 'None')  # Get the default value or None
        init_params.append(f"{name}={default_value}")  # Create parameter string

    # Join the parameters into a single string
    init_params_str = ', '.join(init_params)

    # Add the __init__ method definition to class_code
    large_string += (f'{tab}def __init__(self, {init_params_str}):\n')

    # Add attribute assignments for each field in the __init__ method
    for name in field_names:
        large_string += (f'{tab}{tab}self.{name} = {name}')
        large_string += new

    large_string += new  

    # __repr__ method
    large_string += (f'{tab}def __repr__(self):\n')
    repr_fields_list = []  

    for name in field_names:  # Loop through each field name
        repr_field = (f'{name}={{self.{name}!r}}')  # Create the representation for the field
        repr_fields_list.append(repr_field)  # Append the field representation to the list

    # Join the list of field representations into a single string
    repr_fields = ','.join(repr_fields_list)

    # Format the full representation string
    repr_str = (f'{type_name}({repr_fields})') 

    large_string += (f"{tab}return f'{repr_str}'\n\n")
    large_string += new
    large_string += new

    # Accessor methods
    for name in field_names:
        large_string += f"    def get_{name}(self):\n"
        large_string += f"        return self.{name}\n\n"

        # __getitem__ method
    large_string += "    def __getitem__(self, index):\n"
    large_string += f"        return getattr(self, self._fields[index])\n\n"

        # __eq__ method
    large_string += "    def __eq__(self, other):\n"
    large_string += "        if not isinstance(other, self.__class__):\n"
    large_string += "            return NotImplemented\n"
    large_string += "        return all(getattr(self, name) == getattr(other, name) for name in self._fields)\n\n"

        # asdict method
    large_string += "    def asdict(self):\n"
    large_string += "        return {name: getattr(self, name) for name in self._fields}\n\n"

        # make method
    large_string += "    @classmethod\n"
    large_string += "    def make(cls, iterable):\n"
    large_string += "        return cls(*iterable)\n\n"

        # replace method
    large_string += "    def replace(self, **kwargs):\n"
    large_string += "        if self._mutable:\n"
    large_string += "            for name, value in kwargs.items():\n"
    large_string += "                setattr(self, name, value)\n"
    large_string += "            return None\n"
    large_string += "        else:\n"
    large_string += "            new_values = {name: kwargs.get(name, getattr(self, name)) for name in self._fields}\n"
    large_string += "            return self.__class__(**new_values)\n\n"

        # __setattr__ method
    large_string += "    def __setattr__(self, name, value):\n"
    large_string += "        if not self._mutable and name in self._fields and hasattr(self, name):\n"
    large_string += "            raise AttributeError(f'Cannot modify {name} in immutable {self.__class__.__name__}')\n"
    large_string += "        super().__setattr__(name, value)\n"

        # Execute the generated class code
    namespace = {}
    exec(large_string, namespace)
    return namespace[type_name]



#TESTS
#coordinate = mynamedtuple('coordinate', ['x','y'], mutable=False) 
#coordinate = mynamedtuple('coordinate', 'x y')
#p = coordinate(0, 0)
#print(p) # coordinate(x=0,y=0)
#print(p.asdict()) #{’x’: 0, ’y’: 0}
