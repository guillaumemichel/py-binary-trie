import unittest

from trie import Trie
from helpers import int_to_bitstring
from encoding import encode_bitstring, decode_bitstring, bitstring_to_varint, varint_to_bitstring


class TestStringMethods(unittest.TestCase):
    def test_simple_trie(self):
        t = Trie()
        nodeIDs = [2, 3, 4, 6, 7, 9, 11, 13]
        for i in nodeIDs:
            self.assertTrue(t.add(int_to_bitstring(i, 4)))

        self.assertFalse(t.add(int_to_bitstring(2, 4)))

        self.assertEqual(t.size, 8)

        self.assertTrue(t.contains("0010"))
        self.assertEqual(t.contains("0001"), False)
        self.assertEqual(t.contains("00100"), False)

        self.assertEqual(t.depth(""), 0)
        self.assertEqual(t.depth("0"), 1)
        self.assertEqual(t.depth("001"), 2)
        self.assertEqual(t.depth("0010"), 3)
        self.assertEqual(t.depth("0011"), 3)
        self.assertEqual(t.depth("0100"), 3)
        self.assertEqual(t.depth("011"), 3)
        self.assertEqual(t.depth("0110"), 4)
        self.assertEqual(t.depth("0111"), 4)
        self.assertEqual(t.depth("1"), 1)
        self.assertEqual(t.depth("1101"), 2)
        self.assertEqual(t.depth("10"), 2)
        self.assertEqual(t.depth("11"), -1)
        self.assertEqual(t.depth("0000"), -1)

        self.assertEqual(t.n_closest_keys("0010", 1), ["0010"])
        self.assertEqual(t.n_closest_keys("0010", 3), ["0010", "0011", "0110"])
        self.assertEqual(t.n_closest_keys("0010", 8), ["0010", "0011", "0110", "0111", "0100", "1011", "1001", "1101"])
        self.assertEqual(t.n_closest_keys("0010", 25), ["0010", "0011", "0110", "0111", "0100", "1011", "1001", "1101"])

        self.assertEqual(t.find_trie("011").size, 2)
        self.assertEqual(t.find_trie("0110").size, 1)
        self.assertEqual(t.find_trie("0111").size, 1)
        self.assertEqual(t.find_trie("").size, 8)
        self.assertEqual(t.find_trie("0").size, 5)
        self.assertEqual(t.find_trie("001").size, 2)

        self.assertEqual(len(t.match_prefix_keys("")), len(nodeIDs))
        self.assertEqual(t.match_prefix_keys("00"), ["0010", "0011"])
        self.assertEqual(t.match_prefix_keys("0000"), [])
        self.assertEqual(t.match_prefix_keys("0100"), ["0100"])
        self.assertEqual(t.match_prefix_keys("1"), ["1001", "1011", "1101"])

    def test_simple_metadata_trie(self):
        class SimpleObj(object):
            def __init__(self, key, name, some_bool):
                self.key = key
                self.name = name
                self.some_bool = some_bool

        t = Trie(SimpleObj)
        nodeIDs = [2, 3, 4, 6, 7, 9, 11, 13]

        objs = []
        for i in nodeIDs:
            objs.append(SimpleObj(int_to_bitstring(i, 4), "Node " + str(i), i % 3 == 0))
            self.assertTrue(t.add(int_to_bitstring(i, 4), metadata=objs[-1]))

        self.assertFalse(t.add(int_to_bitstring(2, 4), metadata=objs[0]))

        self.assertEqual(t.size, 8)

        self.assertEqual(t.find("0010"), objs[0])
        self.assertEqual(t.find("0001"), None)
        self.assertEqual(t.find("00100"), None)

        self.assertEqual(t.n_closest("0010", 1), [objs[0]])
        self.assertEqual(t.n_closest("0010", 3), [objs[0], objs[1], objs[3]])
        self.assertEqual(t.n_closest("0010", 3, predicate=lambda n: n.some_bool), [objs[1], objs[3], objs[5]])
        self.assertEqual(
            t.n_closest("0010", 8), [objs[0], objs[1], objs[3], objs[4], objs[2], objs[6], objs[5], objs[7]]
        )
        self.assertEqual(
            t.n_closest("0010", 25), [objs[0], objs[1], objs[3], objs[4], objs[2], objs[6], objs[5], objs[7]]
        )

        self.assertEqual(t.find("0011").name, "Node 3")
        self.assertEqual(t.find("0011").key, int_to_bitstring(3, 4))

        self.assertEqual(t.find_trie("011").size, 2)
        self.assertEqual(t.find_trie("0110").size, 1)
        self.assertEqual(t.find_trie("0111").size, 1)
        self.assertEqual(t.find_trie("").size, 8)
        self.assertEqual(t.find_trie("0").size, 5)
        self.assertEqual(t.find_trie("001").size, 2)

        self.assertEqual(len(t.match_prefix("")), len(nodeIDs))
        self.assertEqual(t.match_prefix("00"), objs[:2])
        self.assertEqual(t.match_prefix("00"), t.match_prefix("001"))
        self.assertEqual(t.match_prefix("0000"), [])
        self.assertEqual(t.match_prefix("0100"), [objs[2]])
        self.assertEqual(t.match_prefix("1"), objs[-3:])
        self.assertEqual(t.match_prefix("1", predicate=lambda n: n.some_bool), [objs[-3]])

    def test_encoding(self):
        self.assertEqual(encode_bitstring(""), 0)
        self.assertEqual(encode_bitstring("0"), 1)
        self.assertEqual(encode_bitstring("1"), 2)
        self.assertEqual(encode_bitstring("00"), 3)
        self.assertEqual(encode_bitstring("01"), 4)
        self.assertEqual(encode_bitstring("10"), 5)
        self.assertEqual(encode_bitstring("11"), 6)
        self.assertEqual(encode_bitstring("000"), 7)
        self.assertEqual(encode_bitstring("0000"), 15)
        self.assertEqual(encode_bitstring("0000000"), 127)
        self.assertEqual(encode_bitstring("0000001"), 128)

        self.assertEqual(decode_bitstring(0), "")
        self.assertEqual(decode_bitstring(1), "0")
        self.assertEqual(decode_bitstring(2), "1")
        self.assertEqual(decode_bitstring(3), "00")
        self.assertEqual(decode_bitstring(4), "01")
        self.assertEqual(decode_bitstring(5), "10")
        self.assertEqual(decode_bitstring(6), "11")
        self.assertEqual(decode_bitstring(7), "000")
        self.assertEqual(decode_bitstring(15), "0000")
        self.assertEqual(decode_bitstring(127), "0000000")
        self.assertEqual(decode_bitstring(128), "0000001")

        for i in range(2**16):
            self.assertEqual(encode_bitstring(decode_bitstring(i)), i)
            self.assertEqual(decode_bitstring(encode_bitstring(int_to_bitstring(i, 16))), int_to_bitstring(i, 16))

        self.assertEqual(bitstring_to_varint("0"), (1).to_bytes(1, "big"))
        self.assertEqual(bitstring_to_varint("0000000"), (127).to_bytes(1, "big"))
        self.assertEqual(bitstring_to_varint("0000001"), (2**15 + 1).to_bytes(2, "big"))

        for i in range(2**16):
            bs = int_to_bitstring(i, 16)
            self.assertEqual(varint_to_bitstring(bitstring_to_varint(bs)), bs)


if __name__ == "__main__":
    unittest.main()
