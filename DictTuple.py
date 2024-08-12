from collections import namedtuple
import mynamedtuple

class DictTuple:
    def __init__(self):
        pass

    def __len__(self):
        pass

    def __bool__(self):
        pass

    def __repr__(self):
        pass

coordinate = mynamedtuple('coordinate', 'x y')
d = DictTuple({'c1': coordinate(1, 2)}, {'c1': coordinate(3, 4)})
print(d)
