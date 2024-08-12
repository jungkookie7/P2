import keyword

def mynamedtuple(type_name, field_names, mutable=False, defaults={}):
    # testing type_name
    if type(type_name) != str: 
        raise SyntaxError('not a string')
    elif not type_name[0].isalpha():  
        raise SyntaxError('first element not a letter')
    elif keyword.iskeyword(type_name):  
        raise SyntaxError('first element is a keyword')
    else:  
        pass
    
    # testing field_names
    if type(field_names) == str: 
        field_names = field_names.replace(',', ' ').split()

    if type(field_names) != list or len(field_names) == 0:  
        raise SyntaxError('not list OR empty')

    for i in field_names:
        if not i[0].isalpha():  
            raise SyntaxError('first element not a letter')
        elif keyword.iskeyword(i):  
            raise SyntaxError('first element is a keyword')
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
        raise SyntaxError('not a dict')
    
    for i in defaults:
        if i not in field_names:  
            raise SyntaxError ('element i not a field_names')
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
    parameters = ''
    for i in field_names:
        parameters += (f"{i}={defaults.get(i, 'None')}, ")
    parameters = parameters[:-2]
    big_string += (f'{tab}def __init__(self, {parameters}):')
    big_string += f'{new}'
    
    for i in field_names:
        big_string += (f'{tab*2}self.{i} = {i}{new}')
    big_string += new
    #print(big_string) *TEST MIDWAY

    # __repr__ 
    big_string += (f'{tab}def __repr__(self):')
    big_string += f'{new}'
    losing_it = ''
    for i in field_names:
        losing_it += f"{i}={{self.{i}!r}},"
    losing_it = losing_it.rstrip(', ')  
    big_string += f"{tab*2}return f'{type_name}({losing_it})'"
    big_string += f'{new*2}'
    #print(big_string) *TEST MIDWAY

    # query/accesors 
    for i in field_names:
        big_string += (f'{tab}def get_{i}(self):')
        big_string += f'{new}'
        big_string += (f'{tab*2}return self.{i}')
        big_string += f'{new*2}'
    #print(big_string) *TEST MIDWAY

    # __getitem__ 
    big_string += (f'{tab}def __getitem__(self, index):')
    big_string += f'{new}'
    big_string += (f'{tab*2}return getattr(self, self._fields[index])')
    big_string += f'{new*2}'
    #print(big_string) *TEST MIDWAY

    # __eq__
    big_string += (f'{tab}def __eq__(self, other):')
    big_string += f'{new}'
    big_string += (f'{tab*2}if type(other) != self.__class__:')
    big_string += f'{new}'
    big_string += (f'{tab*3}return False')
    big_string += f'{new}'
    big_string += (f'{tab*2}for name in self._fields:')
    big_string += f'{new}'
    big_string += (f'{tab*3}if getattr(self, name) != getattr(other, name):')
    big_string += f'{new}'
    big_string += (f'{tab*4}return False')
    big_string += f'{new}'
    big_string += (f'{tab*2}return True')
    big_string += f'{new*2}'
    #print(big_string) *TEST MIDWAY

    # asdict 
    big_string += (f'{tab}def _asdict(self):')
    big_string += f'{new}'
    big_string += (f'{tab*2}result = {{')
    big_string += f'{new}'
    big_string += (f'{tab*3}name: getattr(self, name)')
    big_string += f'{new}'
    big_string += (f'{tab*3}for name in self._fields')
    big_string += f'{new}'
    big_string += (f'{tab*2}}}')
    big_string += f'{new}'
    big_string += (f'{tab*2}return result')
    big_string += f'{new*2}'
    #print(big_string) *TEST MIDWAY

    # _make 
    big_string += (f'{tab}@classmethod{new}')
    big_string += (f'{tab}def _make(banana, iterable):{new}')
    big_string += (f'{tab*2}return banana(*iterable){new*2}')
    #print(big_string) *TEST MIDWAY

    # replace 
    big_string += (f'{tab}def replace(self, **kwargs):{new}')
    big_string += (f'{tab*2}pass{new}')
    #print(big_string) 
    #WHY IS IT NOT WORKING

    # _replace 
    big_string += (f'{tab}def _replace(self, **kwargs):{new}')
    big_string += (f'{tab*2}new_values = {{}}{new}')  
    big_string += (f'{tab*2}for name in self._fields:{new}')
    big_string += (f'{tab*3}if name in kwargs:{new}')
    big_string += (f'{tab*4}new_values[name] = kwargs[name]{new}')
    big_string += (f'{tab*3}else:{new}')
    big_string += (f'{tab*4}new_values[name] = getattr(self, name){new*2}')
    big_string += (f'{tab*2}return self.__class__(**new_values){new*2}')
    #print(big_string) *TEST MIDWAY

    # __setattr__
    big_string += (f'{tab}def __setattr__(self, name, value):{new}')
    big_string += (f'{tab*2}if self._mutable:{new}')
    big_string += (f'{tab*3}object.__setattr__(self, name, value){new}')
    big_string += (f'{tab*2}elif name not in self._fields:{new}')
    big_string += (f'{tab*3}object.__setattr__(self, name, value){new}')
    big_string += (f'{tab*2}elif not hasattr(self, name):{new}')
    big_string += (f'{tab*3}object.__setattr__(self, name, value){new}')
    big_string += (f'{tab*2}else:{new}')
    big_string += (f'{tab*3}raise AttributeError')
    #print(big_string) *TEST MIDWAY

    # exec
    namespace = {}
    exec(big_string, namespace)
    return namespace[type_name]
