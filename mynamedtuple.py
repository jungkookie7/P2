import keyword

def mynamedtuple(type_name, field_names, mutable=False, defaults={}):
    #testing type_name
    if type(type_name) != str:
        print('not a string')
        raise SyntaxError
    elif not type_name[0].isalpha():
        print('first element not a letter')
        raise SyntaxError
    elif keyword.iskeyword(type_name):
        print('conflicts w keywords')
        raise SyntaxError
    else:
        print('type_names test passed')
    
    #testing field_names
    if type(field_names) == str:
        field_names = field_names.replace(',', ' ').split()

    if type(field_names) != list or len(field_names) == 0:
        print('not a list or empty')
        raise SyntaxError

    for i in field_names:
        if not field_names[0].isalpha():
            print('first element not a letter')
            raise SyntaxError
        elif keyword.iskeyword(i):
            print('conflicts w keywords')
            raise SyntaxError
        else:
            print(f'field_names element [{i}] passed')

    #testing defaults
    if type(defaults) != dict:
        print('not a dict')
        raise SyntaxError
    
    for i in defaults:
        if i not in field_names:
            print(f'{i} not in field_name')
            raise SyntaxError
        else:
            print(f'{i} in field_names passed')
    
class coordinate:
    _fields = ['x', 'y']
    _mutable = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        pass

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

coordinate = mynamedtuple('coordinate', ['x','y'], mutable=False) #testing tuple number 1
