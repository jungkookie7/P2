from mynamedtuple import mynamedtuple

class DictTuple:
    def __init__(self, *args):
        self.dt = []

        if len(args) == 0:
            raise AssertionError
        for arg in args:
            if not isinstance(arg, dict):
                raise AssertionError
            if not arg:
                raise AssertionError
            self.dt.append(arg)

    def __len__(self):
        total = 0
        duplicates = []
        for i in self.dt:
            if i not in duplicates:
                duplicates.append(i)
                total += 1
        return total 

    def __bool__(self):
        return len(self.dt) > 1

    def __repr__(self):
        dict_repr = ', '.join(f"{repr(d)}" for d in self.dt)
        return f"DictTuple({dict_repr})"

coordinate = mynamedtuple('coordinate', 'x y')
d = DictTuple({'c1': coordinate(1, 2)}, {'c1': coordinate(3, 4)})
print(d)
