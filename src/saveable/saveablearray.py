from saveable.saveabletype import SaveableType
from saveable.saveableint import U16


def array(array_type, int_type=U16):
    """
    A saveable array type that can hold any number of a single type. Type is observable on adds and removes

    Args:
        array_type: The Saveable object type to store in the array

    Returns:
        A Saveable array type
    """
    class SaveableArray(SaveableType):
        def __init__(self):
            SaveableType.__init__(self)
            self.values = []
            self.array_type = array_type
            self.int_type = int_type

        def __iter__(self, *args, **kwargs):
            """
            Iterates through values of the internal list
            """
            return self.values.__iter__(*args, **kwargs)

        def __getitem__(self, item):
            return self.values[item]

        def __len__(self):
            return len(self.values)

        def __str__(self):
            return str(self.values)

        def set(self, values):
            for value in values:
                if not isinstance(value, array_type):
                    raise ValueError("Value '{}' in array is not of type {}".format(value, array_type))
            self.clear()
            self.values = list(values)

        def index(self, val):
            return self.values.index(val)

        def append(self, val):
            """
            Adds a value to the array and checks to make sure it's Saveable and notifies all observers

            Args:
                val: The array_type value to add
            """
            self.insert(len(self.values), val)

        def insert(self, ind, val):
            if not isinstance(val, array_type):
                try:
                    val = array_type(val)
                except:
                    raise ValueError('{} is not of type {}'.format(val, array_type))
            self.values.insert(ind, val)

        def remove(self, val):
            """
            Removes a value from the internal list and notifies all observers

            Args:
                val: The value to remove
            """
            ind = self.values.index(val)
            self.pop(ind)

        def pop(self, ind):
            """
            Removes a value from the internal list and notifies all observers

            Args:
                val: The value to remove
            """
            val = self.values.pop(ind)
            return val

        def clear(self):
            """
            Removes all values from the internal list and notifies all observers
            :return:
            """
            for ind in range(len(self.values)-1, -1, -1):
                self.pop(ind)

        def load_in_place(self, byte_array):
            self.clear()
            size = self.int_type.from_byte_array(byte_array)
            for _ in range(size.value):
                obj = array_type.from_byte_array(byte_array)
                self.append(obj)

        def to_byte_array(self):
            size = self.int_type()
            size.set(len(self.values))
            _array = size.to_byte_array()
            for val in self.values:
                _array += val.to_byte_array()
            return _array

    return SaveableArray


if __name__ == '__main__':
    ArrayType = array(U16)
    a = ArrayType()
    for i in range(10):
        a.append(U16(i))
    print(a)
    b = a.to_byte_array()
    print(b)
    a.load_in_place(b)
    print(a)