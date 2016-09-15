"""
TODO

@date: 8/31/2016
@author: Aleksandr Bezobchuk
@license: MIT
"""
class HashTable:

    # 64-bit FNV prime
    FNV_PRIME = 1099511628211

    # Default hash table capacity
    DEFAULT_CAPACITY = 1024

    # Default hash table load factor
    DEFAULT_LOAD_FACTOR = 0.9

    KEY_IDX = 0
    VALUE_IDX = 1
    HASH_INDEX_IDX = 2

    def __init__(self, capacity=DEFAULT_CAPACITY, load_factor=DEFAULT_LOAD_FACTOR):
        self.size = 0
        self.__load_factor = load_factor
        self.__capacity = capacity
        self.__table = [None for i in range(self.__capacity)]

    # ----------------------------------------------------------------------- #
    #                             Public methods                              #
    # ----------------------------------------------------------------------- #

    def get(self, key):
        """Finds a corresponding value for a given key in the hash table.

        Keyword arguments:
        key - the key to search for
        """

        probe_index = self.__probe(key)

        if self.__table[probe_index]:
            return self.__table[probe_index][HashTable.VALUE_IDX]
        else:
            return None

    def insert(self, key, value):
        """Inserts or updates a key value pair in the hash table. Note, the
        hash value, key, and value are stored. If a collision occurs, we probe
        linearly until an empty slot is found.

        Keyword arguments:
        key - the key to store
        value - the value to store
        """

        probe_index = self.__probe(key)
        hash_value = self.__hash(key)
        hash_index = hash_value % self.__capacity
        hash_entry = (key, value, hash_index)

        if not self.__table[probe_index]:
            # Create new hash table entry
            self.__table[probe_index] = hash_entry

            self.size += 1

            if self.__needs_rebuilding():
                self.__rebuild()
        else:
            # Update existing hash table entry
            self.__table[probe_index] = hash_entry

        return value

    def delete(self, key):
        """Deletes a key value pair from the hash table. When an entry is
        deleted, the succeeding chain may need to be restored to make sure
        future reads and writes work correctly.

        Keyword arguments:
        key - the key to delete
        """

        probe_index = self.__probe(key)
        value = None

        if self.__table[probe_index]:
            value = self.__table[probe_index][HashTable.VALUE_IDX]

            # Delete hash entry
            self.__table[probe_index] = None
            self.size -= 1

            # Restore probe chain
            self.__restore_chain(probe_index)

        return value

    def keys(self):
        """Retrieves all the keys in the hash table using a generator.
        """

        for i in range(self.__capacity):
            if self.__table[i]:
                yield self.__table[i][HashTable.KEY_IDX]

    def values(self):
        """Retrieves all the values in the hash table using a generator.
        """

        for i in range(self.__capacity):
            if self.__table[i]:
                yield self.__table[i][HashTable.VALUE_IDX]

    def items(self):
        """Retrieves all the key, value pairs in the hash table using a
        generator.
        """

        for i in range(self.__capacity):
            if self.__table[i]:
                yield (self.__table[i][HashTable.KEY_IDX], self.__table[i][HashTable.VALUE_IDX])

    # ----------------------------------------------------------------------- #
    #                             Private methods                             #
    # ----------------------------------------------------------------------- #

    def __needs_rebuilding(self):
        """Determines if the hash table size exceeds the load factor.
        """

        if float(self.size) / float(self.__capacity) >= self.__load_factor:
            return True
        else:
            return False

    def __rebuild(self):
        """Rebuilds the hash table by increasing it's size by a constant factor
        and rehashing all existing elements.

        Note: The hash table is rebuilt by creating a secondary larger table
        and inserting existing hash table entries into the new table. This is
        not ideal for performance.
        """

        old_table = self.__table
        old_capacity = self.__capacity

        # Increase table capacity and create new table
        self.__capacity *= 2
        self.__table = [None for i in range(self.__capacity)]

        for i in range(old_capacity):
            if old_table[i]:
                key = old_table[i][HashTable.KEY_IDX]
                value = old_table[i][HashTable.VALUE_IDX]

                probe_index = self.__probe(key)
                hash_value = self.__hash(key)
                hash_index = hash_value % self.__capacity
                hash_entry = (key, value, hash_index)

                self.__table[probe_index] = hash_entry

        del old_table

    def __restore_chain(self, idx):
        """Restores a probe chain by searching forward through the following
        cells of the table until finding either another empty cell or a key
        that can be moved to cell in question.

        Keyword arguments:
        idx - the index to start restoration at
        """

        probe_index = (idx + 1) % self.__capacity

        while True:
            if not self.__table[probe_index]:
                return
            elif self.__table[probe_index][HashTable.HASH_INDEX_IDX] <= idx:
                # Replace cell
                self.__table[idx] = self.__table[probe_index]

                # Empty out cell
                self.__table[probe_index] = None

                # Continue restore at new chain position
                idx = probe_index

            probe_index += 1

    def __probe(self, key):
        """Find the appropriate cell in the table for the corresponding key. A
        valid cell is one that is either empty or has a matching key.

        Keyword arguments:
        key - the key to find an empty cell for
        """

        hash_value = self.__hash(key)
        hash_index = hash_value % self.__capacity

        while True:
            if not self.__table[hash_index] or self.__table[hash_index][HashTable.KEY_IDX] == key:
                return hash_index

            hash_index = (hash_index + 1) % self.__capacity

    def __hash(self, key):
        """Determines a hash value using a hashing function given a specified
        key that is to be used to determine the location in the hash table. The
        FNV-1a hashing function is used. A ID of the object (key) is used to
        build the hash value.

        @see: http://www.isthe.com/chongo/tech/comp/fnv/#FNV-1a

        Keyword arguments:
        key - the key value to hash
        """

        # 64-bit FNV offset (initial hash value)
        hash_value = 14695981039346656037

        for x in str(id(key)):
          hash_value ^= int(x)
          hash_value *= HashTable.FNV_PRIME

        return hash_value
