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

#TESTS
coordinate = mynamedtuple('coordinate', ['x','y'], mutable=False) 
coordinate = mynamedtuple('coordinate', 'x y')
p = coordinate(0, 0)
print(p) # coordinate(x=0,y=0)
print(p.asdict()) #{’x’: 0, ’y’: 0}
