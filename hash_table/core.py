"""
TODO

@date: 8/31/2016
@author: Aleksandr Bezobchuk
@license: MIT
"""
class HashTable:

    # Sentinel value for deleted keys
    TERMINATOR = 0
    # 64-bit FNV prime
    FNV_PRIME = 1099511628211

    DEFAULT_CAPACITY = 1024
    DEFAULT_LOAD_FACTOR = 0.9

    def __init__(self, capacity=DEFAULT_CAPACITY, lf=DEFAULT_LOAD_FACTOR):
        self.__load_factor = lf
        self.__capacity = capacity
        self.__size = 0
        self.__table = [None for i in range(self.__capacity)]

    # ----------------------------------------------------------------------- #
    #                             Public methods                              #
    # ----------------------------------------------------------------------- #

    def insert(self, k, v):
        slot = self.__find_slot(k)

        if self.__table[slot]:
            # Update value in existing element
            self.__table[slot] = (k, v)
        else:
            if self.__needs_rebalancing():
                self.__rebalance()

            slot = self.__find_slot(k)
            self.__table[slot] = (k, v)
            self.__size += 1

        return v

    def get(self, k):
        pass

    def delete(self, k):
        pass

    # ----------------------------------------------------------------------- #
    #                             Private methods                             #
    # ----------------------------------------------------------------------- #

    def __needs_rebalancing(self):
        """TODO
        """

        if float(self.__size) / self.__capacity >= self.__load_factor:
            return True
        else:
            return False

    def __rebalance(self):
        """TODO
        """

        pass

    def __find_slot(self, k):
        """Find the appropriate slot in the table for the corresponding key. If
        a collision occurs, slots are probed using Robin Hood open addressing
        (linear) to find the next best slot.

        Keyword arguments:
        k - the key to find a slot for
        """

        pass

    def __hash(self, k):
        """Determines a hash value using a hashing function given a specified key
        that is to be used to determine the location in the hash table. The FNV-1a
        hashing function is used. A ID of the object (key) is used to build the
        hash value.

        @see: http://www.isthe.com/chongo/tech/comp/fnv/#FNV-1a

        Keyword arguments:
        k -- the key value to hash
        """

        # 64-bit FNV offset (initial hash value)
        hash_value = 14695981039346656037

        for x in str(id(key)):
          hash_value ^= int(x)
          hash_value *= HashTable.FNV_PRIME

        return hash_value % self.__capacity
