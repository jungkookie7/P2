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
    
class coordinate:
    _fields = ['x', 'y']
    _mutable = False

    def __init__(self, type_name, field_names, mutable = False, defaults={}):
        self.type_name = type_name
        self._fields = field_names.split()
        self._mutable = mutable
        self.defaults = defaults
        
        # Dynamically create the __init__ method
        init_code = "def __init__(self, " + ", ".join(
            f"{field}={defaults.get(field, '')!r}" if field in defaults else field
            for field in self._fields
        ) + "):\n"
        
        # Initialize fields
        for field in self._fields:
            init_code += f"    self.{field} = {field}\n"
        
        # Execute the dynamically created __init__ method
        exec(init_code, globals(), locals())
        self.__init__ = locals()['__init__']

    def __repr__(self):
        fields_repr = ", ".join(f"{field}={repr(getattr(self, field))}" for field in self._fields)
        return f"{self.type_name}({fields_repr})"
    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

#TESTERS
coordinate = mynamedtuple('coordinate', ['x','y'], mutable=False) #testing tuple number 1
