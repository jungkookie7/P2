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
    a = []
    seen = {}  

    for name in field_names:
        if name not in seen:
            a.append(name)
            seen[name] = True  
    field_names = a

    #testing defaults
    if type(defaults) != dict: #tests if default is a str
        raise SyntaxError
    
    for i in defaults:
        if i not in field_names: #tests if element is in field_name
            raise SyntaxError
        else: #passes all tests
            pass
    
    #new line and tab
    new = ('\n')
    tab = ('    ')

    #class code
    class_code = (f'class {type_name}:')
    class_code += new
    class_code += (f'{tab}_fields = {field_names}')
    class_code += new
    class_code += (f'{tab}_mutable = {mutable}')
    class_code += new

    # __init__
    class_code += (f'{tab}def __init__(self')

    for name in field_names:
        default_value = defaults.get(name, 'None')  # Get the default value or None
        class_code += f", {name}={default_value!r}"  # Add the parameter to the method signature

    class_code += "):\n"  # End of method signature

    # Assign each parameter to the corresponding instance attribute
    for name in field_names:
        class_code += f"        self.{name} = {name}\n"  # Set the attribute

    class_code += "\n"  # Add a newline after the method


    # __repr__ 
    class_code += "    def __repr__(self):\n"

    # Prepare the field representations
    field_representations = []
    for name in field_names:
        field_representation = f"{name}={{self.{name}!r}}"
        field_representations.append(field_representation)

    # Join the field representations into a single string
    repr_fields = ','.join(field_representations)

    # Format the full representation string
    repr_str = f"{type_name}({repr_fields})"

    class_code += f"        return f'{repr_str}'\n\n"  # Return the formatted string


    # Accessor methods
    for name in field_names:
        class_code += f"    def get_{name}(self):\n"
        class_code += f"        return self.{name}\n\n"

    # __getitem__ method
    class_code += "    def __getitem__(self, index):\n"
    class_code += f"        return getattr(self, self._fields[index])\n\n"

    # __eq__ method
    class_code += "    def __eq__(self, other):\n"
    class_code += "        if not isinstance(other, self.__class__):\n"
    class_code += "            return NotImplemented\n"
    class_code += "        return all(getattr(self, name) == getattr(other, name) for name in self._fields)\n\n"

    # asdict method
    class_code += "    def asdict(self):\n"
    class_code += "        return {name: getattr(self, name) for name in self._fields}\n\n"

    # make method
    class_code += "    @classmethod\n"
    class_code += "    def make(cls, iterable):\n"
    class_code += "        return cls(*iterable)\n\n"

    # replace method
    class_code += "    def replace(self, **kwargs):\n"
    class_code += "        if self._mutable:\n"
    class_code += "            for name, value in kwargs.items():\n"
    class_code += "                setattr(self, name, value)\n"
    class_code += "            return None\n"
    class_code += "        else:\n"
    class_code += "            new_values = {name: kwargs.get(name, getattr(self, name)) for name in self._fields}\n"
    class_code += "            return self.__class__(**new_values)\n\n"

    # __setattr__ method
    class_code += "    def __setattr__(self, name, value):\n"
    class_code += "        if not self._mutable and name in self._fields and hasattr(self, name):\n"
    class_code += "            raise AttributeError(f'Cannot modify {name} in immutable {self.__class__.__name__}')\n"
    class_code += "        super().__setattr__(name, value)\n"

    # Execute the generated class code
    namespace = {}
    exec(class_code, namespace)
    return namespace[type_name]

#TESTERS
coordinate = mynamedtuple('coordinate', ['x','y'], mutable=False) #testing tuple number 1
coordinate = mynamedtuple('coordinate', 'x y')
p = coordinate(0, 0)
print(p) # coordinate(x=0,y=0)
print(p.asdict()) #{’x’: 0, ’y’: 0}
