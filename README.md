# Binary Trie

Python binary trie implementation, helping with XOR distances.

Author: [Guillaume Michel](https://github.com/guillaumemichel)

## Purpose

[IPFS](https://ipfs.network) and [libp2p](https://libp2p.io/) are built upon the Kademlia DHT, which uses the XOR distance as a distance metric between keys. As explained in this [blogpost](https://metaquestions.me/2014/08/01/shortest-distance-between-two-points-is-not-always-a-straight-line/), the XOR distance is tricky to understand and represent. This distance metric is odd for it is non linear.
For instance, $2 \oplus 3 = 1$ but $3 \oplus 4 = 7$. Ordering $N_8$ by XOR distance to 2 gives the following result: $[2,3,0,1,6,7,4,5]$

One popular representation for XOR distance is the Binary Trie. A binary brie is a simple [Trie](https://en.wikipedia.org/wiki/Trie) with keyspace {$0,1$}$^n$ with $n$ being the size of the keyspace. The perfect visual representation of the XOR distance would be a N-dimensional binary trie. The example below displays a binary trie containing the keys $[2,3,4,6,7,9,11,13]$.

![Alt text](./resources/trie.svg)

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
trie.find("0010") # True
trie.find("0100") # False
```

### Finding the closest keys to a target
The `n_closest(key, n)` method returns the `n` closest keys to the provided key in the trie, according to the XOR distance. The keys are sorted according to the distance to the target key. Note that only leaves of the trie will be returned, not intermediary nodes.
```python
trie.n_closest("0001", 1) # ["0000"]
trie.n_closest("0010", 3) # ["0010", "0011", "0000"]
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