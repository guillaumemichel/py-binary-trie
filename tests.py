import unittest

from trie import Trie
from helpers import bytes_to_bitstring, bitstring_to_bytes, int_to_bitstring, bitstring_to_int

class TestStringMethods(unittest.TestCase):

    def test_simple_trie(self):
        t = Trie()
        nodeIDs = [2,3,4,6,7,9,11,13]
        for i in nodeIDs:
            self.assertTrue(t.add(int_to_bitstring(i, 4)))

        self.assertFalse(t.add(int_to_bitstring(2, 4)))

        self.assertEqual(t.size, 8)

        self.assertTrue(t.find("0010"))
        self.assertEqual(t.find("0001"), False)
        self.assertEqual(t.find("00100"), False)

        self.assertEqual(t.n_closest("0010", 1), ["0010"])
        self.assertEqual(t.n_closest("0010", 3), ["0010", "0011", "0110"])
        self.assertEqual(t.n_closest("0010", 8), ["0010", "0011", "0110", "0111", "0100", "1011", "1001", "1101"])
        self.assertEqual(t.n_closest("0010", 25), ["0010", "0011", "0110", "0111", "0100", "1011", "1001", "1101"])

        self.assertEqual(t.find_trie("011").size, 2)
        self.assertEqual(t.find_trie("0110").size, 1)
        self.assertEqual(t.find_trie("0111").size, 1)
        self.assertEqual(t.find_trie("").size, 8)
        self.assertEqual(t.find_trie("0").size, 5)
        self.assertEqual(t.find_trie("001").size, 2)


    def test_simple_metadata_trie(self):
        class SimpleObj(object):
            def __init__(self, key, name):
                self.key = key
                self.name = name

        t = Trie()
        nodeIDs = [2,3,4,6,7,9,11,13]

        objs = []
        for i in nodeIDs:
            objs.append(SimpleObj(int_to_bitstring(i, 4),"Node "+str(i)))
            self.assertTrue(t.add(int_to_bitstring(i, 4), metadata=objs[-1]))

        self.assertFalse(t.add(int_to_bitstring(2, 4), metadata=objs[0]))

        self.assertEqual(t.size, 8)

        self.assertEqual(t.find("0010"), objs[0])
        self.assertEqual(t.find("0001"), False)
        self.assertEqual(t.find("00100"), False)

        self.assertEqual(t.n_closest("0010", 1), [objs[0]])
        self.assertEqual(t.n_closest("0010", 3), [objs[0], objs[1], objs[3]])
        self.assertEqual(t.n_closest("0010", 8), [objs[0], objs[1], objs[3], objs[4], objs[2], objs[6], objs[5], objs[7]])
        self.assertEqual(t.n_closest("0010", 25), [objs[0], objs[1], objs[3], objs[4], objs[2], objs[6], objs[5], objs[7]])

        self.assertEqual(t.find("0011").name, "Node 3")
        self.assertEqual(t.find("0011").key, int_to_bitstring(3, 4))

        self.assertEqual(t.find_trie("011").size, 2)
        self.assertEqual(t.find_trie("0110").size, 1)
        self.assertEqual(t.find_trie("0111").size, 1)
        self.assertEqual(t.find_trie("").size, 8)
        self.assertEqual(t.find_trie("0").size, 5)
        self.assertEqual(t.find_trie("001").size, 2)



if __name__ == '__main__':
    unittest.main()