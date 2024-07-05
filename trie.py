from typing import TypeVar, List, Callable, Optional, Generic

T = TypeVar("T")


class Trie(Generic[T]):
    def __init__(self, metadata=Optional[T], key: str = "", depth: int = 0):
        self.metadata = metadata
        self.key = key  # eg. "01110101"
        self.branch: List[Optional[Trie], Optional[Trie]] = [None, None]
        self.dpt = depth
        self.size = 0  # only counts the leaves

    def __repr__(self) -> str:
        # "(branch[0].key / self.key \ branch[1].key)"
        rep = "("
        if self.branch[0] is not None:
            rep += self.branch[0].key + " / "
        rep += self.key
        if self.branch[1] is not None:
            rep += " \\ " + self.branch[1].key
        return rep + ")"

    # add the provided key to the trie
    # returns True on success and False on failure (usually
    # when the key is already in the trie)
    def add(self, key: str, metadata: Optional[T] = None) -> bool:
        if self.branch[int(key[len(self.key)])] is not None:
            # branch already exists
            branch = self.branch[int(key[len(self.key)])]

            minLen = min(len(key), len(branch.key))
            if key[:minLen] == branch.key[:minLen]:
                if len(key) == len(branch.key):
                    # key already in the trie, cannot insert it
                    return False
                else:
                    # key is a branch of branch
                    #
                    #     11  +insert(111001)  *111* +insert(111001)
                    #    /  \                  /   \
                    # 110  *111*     -->     1110  1111

                    success = branch.add(key=key, metadata=metadata)
            else:
                # insert between two nodes in the trie
                #
                #   11 +insert(111001)     11 self
                #  / \                    / \
                #     \       -->          1110 mid
                #      \                  /    \
                #     111011     key 111001 111011 branch

                for i in range(minLen):
                    if branch.key[i] != key[i]:
                        # first bit where branch.key and key diverge

                        # create mid Trie node
                        mid = Trie(key=branch.key[:i], depth=self.dpt + 1)
                        # define mid branches
                        # create new trie node
                        mid.branch[int(key[i])] = Trie(metadata=metadata, key=key, depth=self.dpt + 2)
                        mid.branch[int(key[i])].size = 1
                        mid.branch[1 - int(key[i])] = branch
                        # update branch depth
                        branch.incr_depth()
                        # set its size
                        mid.size = branch.size + 1
                        # update self branch to mid
                        self.branch[int(key[len(self.key)])] = mid
                        success = True

                        break
        else:
            # self doesn't have the appropriate branch
            # only useful for root node
            #
            #    . +insert(001)  .            . +insert(110)   .
            #         -->       /     OR     /      -->       / \
            #                 001          001              001 110

            self.branch[int(key[len(self.key)])] = Trie(metadata=metadata, key=key, depth=self.dpt + 1)
            self.branch[int(key[len(self.key)])].size = 1
            success = True

        if success:
            self.size += 1
        return success

    def incr_depth(self):
        self.dpt += 1
        for i in range(2):
            if self.branch[i] is not None:
                self.branch[i].incr_depth()

    # returns the trie object matching the given key
    # for internal use only
    def find_trie(self, key: str):
        if len(self.key) >= len(key):
            if self.key == key:
                return self
            else:
                return None
        elif self.branch[int(key[len(self.key)])] is not None:
            return self.branch[int(key[len(self.key)])].find_trie(key)
        else:
            return None

    # returns metadata associated with the key, if the key is in the trie and has metadata
    # returns None if no metadata or key not in trie
    def find(self, key: str) -> Optional[T]:
        trie = self.find_trie(key)
        if trie is None:
            return None
        else:
            return trie.metadata

    # returns True if key in trie, False otherwise
    def contains(self, key: str) -> bool:
        trie = self.find_trie(key)
        return not trie is None

    def depth(self, key: str) -> int:
        trie = self.find_trie(key)
        if trie is None:
            return -1
        else:
            return trie.dpt

    def n_closest_tries(self, key: str, n: int, predicate: Optional[Callable[[T], bool]] = None):
        if self.branch[0] == self.branch[1] == None:
            # leaf of the trie
            if predicate is None or predicate(self.metadata):
                return [self]
            else:
                return []

        nclosest = []
        if self.branch[int(key[len(self.key)])] is not None:
            # get n closest on the closest branch
            nclosest += self.branch[int(key[len(self.key)])].n_closest_tries(key, n, predicate=predicate)
        if len(nclosest) < n and self.branch[1 - int(key[len(self.key)])] is not None:
            # if we don't have n keys yet, get the difference from the other branch
            nclosest += self.branch[1 - int(key[len(self.key)])].n_closest_tries(
                key, n - len(nclosest), predicate=predicate
            )

        return nclosest

    # returns a list of the metadata of the n closest keys in the Trie to the given key
    def n_closest(self, key: str, n: int, predicate: Optional[Callable[[T], bool]] = None) -> List[Optional[T]]:
        return [t.metadata for t in self.n_closest_tries(key, n, predicate)]

    # returns the n closest keys to the provided key
    def n_closest_keys(self, key: str, n: int, predicate: Optional[Callable[[T], bool]] = None) -> List[str]:
        return [t.key for t in self.n_closest_tries(key, n, predicate)]

    # returns the list of all trie leaves of a given trie node
    # for internal use only
    def get_leaves_tries(self, predicate: Optional[Callable[[T], bool]]) -> List:
        if self.branch[0] == self.branch[1] == None:
            # node is leaf, return itself
            if predicate is None or predicate(self.metadata):
                return [self]
            else:
                return []
        leaves = []
        for i in range(2):
            # combine lists returned by right and left branches
            if self.branch[i] is not None:
                leaves += self.branch[i].get_leaves_tries(predicate)
        return leaves

    # returns as list of trie leaves matching the provided prefix
    # for internal use only
    def match_prefix_tries(self, prefix: str, predicate: Optional[Callable[[T], bool]] = None) -> List:
        if len(self.key) >= len(prefix):
            # the target key is a prefix of self key
            if prefix == self.key[: len(prefix)]:
                return self.get_leaves_tries(predicate)
            else:
                return []
        elif self.branch[int(prefix[len(self.key)])] is not None:
            # go down the trie to match the prefix length
            return self.branch[int(prefix[len(self.key)])].match_prefix_tries(prefix, predicate)
        else:
            return []

    # returns the list of metadata of trie leaves matching the provided prefix
    def match_prefix(self, prefix: str, predicate: Optional[Callable[[T], bool]] = None) -> List[Optional[T]]:
        return [t.metadata for t in self.match_prefix_tries(prefix, predicate)]

    # returns the list of keys of trie leaves matching the provided prefix
    def match_prefix_keys(self, prefix: str, predicate: Optional[Callable[[T], bool]] = None) -> List[str]:
        return [t.key for t in self.match_prefix_tries(prefix, predicate)]
