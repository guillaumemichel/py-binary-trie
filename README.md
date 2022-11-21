# Binary Trie

Python binary trie implementation, helping with XOR distances.

Author: [Guillaume Michel](https://github.com/guillaumemichel)

## Purpose

[IPFS](https://ipfs.network) and [libp2p](https://libp2p.io/) are built upon the Kademlia DHT, which uses the XOR distance as a distance metric between keys. As explained in this [blogpost](https://metaquestions.me/2014/08/01/shortest-distance-between-two-points-is-not-always-a-straight-line/), the XOR distance is tricky to understand and represent. This distance metric is odd for it is non linear.
For instance, $2 \oplus 3 = 1$ but $3 \oplus 4 = 7$. Ordering $N_8$ by XOR distance to 2 gives the following result: $[2,3,0,1,6,7,4,5]$

One popular representation for XOR distance is the Binary Trie. A binary brie is a simple [Trie](https://en.wikipedia.org/wiki/Trie) with keyspace $\lbrace0,1\rbrace^n$ with $n$ being the size of the keyspace. The perfect visual representation of the XOR distance would be a N-dimensional binary trie. The example below displays a binary trie containing the keys $[2,3,4,6,7,9,11,13]$.

![Alt text](./resources/trie.svg)

Each node in the Trie can be associated with some metadata for convenience.

## Usage

### Install

```bash
pip install binary-trie
```

### Import

```python
from binary_trie import Trie, bytes_to_bitstring, bitstring_to_bytes, int_to_bitstring, bitstring_to_int
```

### Creating an empty trie
```python
trie = Trie()
```
### Adding keys
The `add(key)` method takes a bitstring as input. The bitstring can either be provided directly, or be computer from an `int` or `bytes` using the `int_to_bitstring()` and `bytes_to_bitstring()` functions. Note that the `l` parameter represent the bit length of the binary representation. It is important that all keys share the same bit length. The bit length can be omitted in `bytes_to_bistring()` when working with bit lengths multiple of 8.
```python
trie.add("0010")
trie.add(4*"0")
trie.add(int_to_bitstring(3, l=4))
trie.add(bytes_to_bitstring(b'\x0e', l=4))
```
The add function returns `True` on success, and `False` if the key was already in the trie (not inserted).

### Finding keys
The `find(key)` method returns `True` if the provided key is in the Trie, `False` otherwise.
```python
trie.contains("0010") # True
trie.contains("0100") # False
```

### Key depth
The `depth(key)` method returns the depth of the provided key, if it is in the Trie and `-1` otherwise. The depth of a trie node is defined as the number of its direct ancestors, up to the root of the trie.
```python
trie.depth("0")    # 1
trie.depth("0010") # 3
trie.depth("0111") # 4
trie.depth("1101") # 2
trie.depth("11")   # -1
```

### Finding the closest keys to a target
The `n_closest_keys(key, n)` method returns the `n` closest keys to the provided key in the trie, according to the XOR distance. The keys are sorted according to the distance to the target key. Note that only leaves of the trie will be returned, not intermediary nodes.
```python
trie.n_closest_keys("0001", 1) # ["0000"]
trie.n_closest_keys("0010", 3) # ["0010", "0011", "0000"]
```

### Prefix matching

The `prefix_match_keys(prefix)` will return the list of keys of all leaves of the Trie matching the provided `prefix`.

```python
trie.prefix_match_keys("00")   # ["0000", "0010", "0011"]
trie.prefix_match_keys("1111") # []
```

### Attaching metadata to Trie nodes

It is possible to attach an `object` as metadata to a trie leaf node.

```python
class MyObj(object):
    def __init__(self, key, name):
        self.key = key
        self.name = name

trie = Trie(MyObj)

obj = MyObj(int_to_bitstring(10, 4), "Node 10")
trie.add(obj.key, obj)

trie.find(obj.key).name        # "Node 10"
trie.n_closest(obj.key, 1)     # [obj]
trie.prefix_match(obj.key[:2]) # [obj]
```
Note that the `find(key)` method is similar to the `contains(key)` method, but returns the associated `metadata` if any, instead of returning a `bool`.
The `n_closest(key, n)` method is similar to the `n_closest_keys(key, n)` method, but returns the list of `metadata` associated with the closest keys, instead of the list of keys.


### Predicates

It is possible to assign some boolean variables to `metadata` objects, and make use of them using predicate in `n_closest()`, `n_closest_keys()`, `prefix_match()` and `prefix_match_keys()` methods to filter the results.

```python
class MyObj(object):
    def __init__(self, key, name, some_bool):
        self.key = key
        self.name = name
        self.some_bool = some_bool

trie = Trie(MyObj)

nodeIDs = [0, 1, 2] # ["0000", "0001", "0010"]
for i in nodeIDs:
    obj = MyObj(int_to_bitstring(i, 4), "Node "+str(i), i % 2 == 0)
    trie.add(obj.key, obj)

trie.n_closest_keys("0001", 2, predicate=lambda n: n.some_bool) # ["0000", "0010"] 
trie.prefix_match_keys("000", predicate=lambda n: n.some_bool)  # ["0000"]

# Note that the key "0001" matched both requests, but wasn't taken into
# consideration as it doesn't satisfy the predicate
```


### Helpers

There are 4 helpers functions to facilitate the use of this implementation with keys being not only `bitstring`, but also `bytes` or `int`. These helper functions help translate `bytes` and `int` to `bitstring` and reciprocally.
```python
def bytes_to_bitstring(data: bytes, l: int=8*len(data)) -> bytes:
    ...
bytes_to_bitstring(b'\xff\x00') # "1111111100000000"
bytes_to_bitstring(b'\xf3',l=4) # "0011"

def bitstring_to_bytes(bs: str) -> bytes:
    ...
bitstring_to_bytes("1111111100000000") # b'\xff\x00'
bitstring_to_bytes("0011")             # b'\x03'

def int_to_bitstring(i, l: int) -> bytes:
    ...
int_to_bitstring(6, 4)  # "0110"
int_to_bitstring(6, 16) # "0000000000000110"

def bitstring_to_int(bs: str) -> int:
    ...
bitstring_to_int("0110")             # 6
bitstring_to_int("0000000000000110") # 6
```
