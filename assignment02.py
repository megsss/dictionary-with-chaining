import unittest

'''
Description:
Author:
Version:
Help provided to: Piper
Help received from: Peter, Piper, Sean
'''

'''
    Implement a dictionary using chaining.
    You may assume every key has a hash() method, e.g.:
    >>> hash(1)
    1
    >>> hash('hello world')
    -2324238377118044897
'''


class dictionary:
    def __init__(self, init=None):
        self.__limit = 10
        self.__items = [[] for _ in range(self.__limit)]
        self.__count = 0

        if init:
            for i in init:
                self.__setitem__(i[0], i[1])

    def slot(self, key):
        return hash(key) % self.__limit

    def __len__(self):
        return self.__count

    def flattened(self):
        return [item for inner in self.__items for item in inner]

    def __iter__(self):
        return (iter(self.flattened()))

    def __str__(self):
        return (str(self.flattened()))

    def __setitem__(self, key, value):
        index = self.slot(key)

        if self.__items[index] == []:
            self.__items[index].append([key, value])
            self.__count += 1
        else:
            for i in self.__items[index]:
                if key is i[0]:
                    i[1] = value
                    return
            self.__items[index].append([key, value])
            self.__count += 1

        if self.__count >= self.__limit * 0.75:
            self.double_rehash()
            return




    def __getitem__(self, key):
        index = self.slot(key)
        for i in self.__items[index]:
            if key == i[0]:
                return i[1]

    def __contains__(self, key):
        index = self.slot(key)
        for i in self.__items[index]:
            if key == i[0]:
                return True
        return False

    def __delitem__(self, key):
        index = self.slot(key)
        item = self.__items[index]
        count = 0
        for i in item:
            if key == i[0]:
                del item[count]
                self.__count -= 1
            count += 1

        if self.__count <= self.__limit * 0.25:
            self.halving_rehash()
            return

    def load(self):
        return self.__count / self.__limit

    def double_rehash(self):
        oldhash = self.flattened()
        self.__limit = self.__limit * 2
        self.__count = 0
        self.__items = [[]] * self.__limit
        for i in oldhash:
            self.__setitem__(i[0], i[1])

    def halving_rehash(self):
        oldhash = self.flattened()
        self.__limit = self.__limit // 2
        self.__count = 0
        self.__items = [[]] * self.__limit
        for i in oldhash:
            self.__setitem__(i[0], i[1])

    def keys(self):
        flattened = self.flattened()
        keylist = []
        for i in flattened:
            keylist.append(i[0])
        return keylist

    def values(self):
        flattened = self.flattened()
        valuelist = []
        for i in flattened:
            valuelist.append(i[1])
        return valuelist

    def __eq__(self, other):
        if self.keys() == other.keys() and self.values() == other.values():
            return True
        else:
            return False

    def items(self):
        pass




''' C-level work '''


class test_add_two(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        self.assertEqual(len(s), 2)
        self.assertEqual(s[1], "one")
        self.assertEqual(s[2], "two")


class test_add_twice(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[1] = "one"
        self.assertEqual(len(s), 1)
        self.assertEqual(s[1], "one")

class test_store_false(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = False
        self.assertTrue(1 in s)
        self.assertFalse(s[1])

class test_store_none(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = None
        self.assertTrue(1 in s)
        self.assertEqual(s[1], None)

class test_none_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[None] = 1
        self.assertTrue(None in s)
        self.assertEqual(s[None], 1)

class test_False_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[False] = 1
        self.assertTrue(False in s)
        self.assertEqual(s[False], 1)

class test_collide(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        self.assertEqual(len(s), 2)
        self.assertTrue(0 in s)
        self.assertTrue(10 in s)

class test_del(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        self.assertEqual(len(s), 3)
        s.__delitem__(1)
        self.assertEqual(len(s), 2)

class rehash(unittest.TestCase):
    def test_halving(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        self.assertEqual(s.load(), 0.3)
        del s[1]
        self.assertEqual(s.load(), 0.4)
    def test_double(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        s[4] = "four"
        s[5] = "five"
        s[6] = "six"
        s[7] = "seven"
        self.assertEqual(s.load(), 0.7)
        s.__setitem__(8, "eight")
        self.assertEqual(s.load(), 0.4)

class check_keys(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        s[4] = "four"
        self.assertEqual(s.keys(), [1, 2, 3, 4])

class check_values(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        s[4] = "four"
        self.assertEqual(s.values(), ["one", "two", "three", "four"])

class check_equal(unittest.TestCase):
    def test_true(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        a = dictionary()
        a[1] = "one"
        a[2] = "two"
        a[3] = "three"
        self.assertTrue(s == a)
    def test_false(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        a = dictionary()
        a[1] = "one"
        a[2] = "two"
        a[4] = "four"
        self.assertFalse(s == a)


''' B-level work
    Add doubling and rehashing when load goes over 75%
    Add __delitem__(self, key)
'''

''' A-level work
    Add halving and rehashing when load goes below 25%
    Add keys()
    Add values()
'''

''' Extra credit
    Add __eq__()
    Add items(), "a list of D's (key, value) pairs, as 2-tuples"
'''

if __name__ == '__main__':
    unittest.main()