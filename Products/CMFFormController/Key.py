from functools import total_ordering

import OFS


@total_ordering
class Key(OFS.SimpleItem.SimpleItem):
    key = None

    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        keylen = len(self.key)
        for i in range(0, keylen - 1):
            if self.key[i] != other.key[i]:
                return self._compare(self.key[i], other.key[i])
        return self._compare(self.key[keylen - 1], other.key[keylen - 1])

    def _compare(self, k1, k2):
        # make None end up last
        if k1 is None and k2 is None:
            return False
        if k2 is None:
            return True
        if k1 is None:
            return False
        return k1 < k2

    def getKey(self):
        return self.key

    def __hash__(self):
        return hash(self.key)
