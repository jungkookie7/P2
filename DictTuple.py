from mynamedtuple import mynamedtuple

class DictTuple:
    def __init__(self, *args):
        self.dt = []

        if len(args) == 0:
            raise AssertionError
        for i in args:
            if type(i) != dict:
                raise AssertionError
            if not i:
                raise AssertionError
            self.dt.append(i)

    def __len__(self):
        keys = 0  
        empty_list = []  

        for dictionary in self.dt:
            for key in dictionary.keys():
                if key not in empty_list:  
                    empty_list.append(key)  
                    keys += 1  
        return keys  

    def __bool__(self):
        if len(self.dt) == 1:
            return False
        else:
            return True

    def __repr__(self):
        another_list = []
        for i in self.dt:
            string_version = repr(i)
            another_list.append(string_version)
        joined_dicts = ', '.join(another_list)
        return (f'DictTuple({joined_dicts})')

    def __contains__(self, key):
        return any(key in d for d in self.dt)

    def __getitem__(self, key):
        for d in reversed(self.dt):
            if key in d:
                return d[key]
        raise KeyError(f"{key} not found in any dictionary.")

    def __setitem__(self, key, value):
        for d in reversed(self.dt):
            if key in d:
                d[key] = value
                return
        self.dt.append({key: value})

    def __delitem__(self, key):
        found = False
        for d in self.dt:
            if key in d:
                del d[key]
                found = True
        if not found:
            raise KeyError(f"{key} not found in any dictionary.")

    def __call__(self, key):
        return [d[key] for d in self.dt if key in d]

    def __iter__(self):
        seen = set()
        for d in reversed(self.dt):
            for key in sorted(d.keys()):
                if key not in seen:
                    seen.add(key)
                    yield key

    def __eq__(self, other):
        if isinstance(other, DictTuple):
            return all(self[key] == other[key] for key in self) and len(self) == len(other)
        elif isinstance(other, dict):
            return all(self[key] == other.get(key) for key in self) and len(self) == len(other)
        return False

    def __add__(self, other):
        if isinstance(other, DictTuple):
            # Filter out empty dictionaries
            combined = [d for d in (*self.dt, *other.dt) if d]
            return DictTuple(*combined)
        elif isinstance(other, dict):
            if other:
                return DictTuple(*self.dt, other)
            else:
                raise AssertionError("Cannot add an empty dictionary to a DictTuple.")
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'DictTuple' and '{type(other).__name__}'")


    def __setattr__(self, name, value):
        if name == "dt":
            super().__setattr__(name, value)
        else:
            raise AssertionError(f"Cannot set attribute {name}; only 'dt' is allowed.")
