# Name: Freddie Main III
# OSU Email: MainF@oregonstate.eud
# Course: CS261 - Data Structures
# Assignment 6: HashMap Implementation
# Due Date: 12/2/22
# Description: Program is an implementation of a Hash Map and core methods for
# interaction.

from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #
    def put(self, key: str, value: object) -> None:
        """
        Description:
            Method takes a key and a value as parameters and updates the hash
            map accordingly. If the key already exists, the value is updated.
            If the passed key is new, a new key/value pair is added.

        Parameters:
            key: passed key value associated with the passed value.

            value: passed object value associated with the passed key.

        Returns:
            None
        """
        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        hashed_key = self._hash_function(key) % self._capacity
        original_index = hashed_key
        bucket = self._buckets[hashed_key]

        count = 1
        while bucket is not None:
            if bucket.is_tombstone:
                break
            if bucket.key == key:
                bucket.value = value
                self._buckets.set_at_index(hashed_key, bucket)
                return
            hashed_key = (original_index + count ** 2) % self._capacity
            bucket = self._buckets[hashed_key]
            count += 1

        # Place the new HashEntry
        self._buckets.set_at_index(hashed_key, HashEntry(key, value))
        self._size += 1

    def table_load(self) -> float:
        """
        Description:
            Method takes no parameters, calculates the current hash table load
            factor, and returns the value.

        Parameters:
            None

        Returns:
            load_factor: current decimal value of the hash table's load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Description:
            Method takes no parameters and returns the number of empty buckets
            in the hash table.

        Parameters:
            None

        Returns:
            empty_count: integer value of the number of empty buckets in the
            hash table.
        """
        empty_count = 0
        for bucket_iterator in range(self._capacity):
            if (self._buckets[bucket_iterator] is None or
                    self._buckets[bucket_iterator].is_tombstone):
                empty_count += 1
        return empty_count

    def resize_table(self, new_capacity: int) -> None:
        """
        Description:
            Method takes a new capacity value as a parameter and resizes the
            internal hash table's capacity to it. If the new capacity is less
            than 1, the method does nothing. If 1 or more, make sure it is
            prime. All existing key/value pairs remain in the new hash map and
            all hash table links are rehashed.

        Parameters:
            new_capacity: integer value of the new capacity of the internal
            hash table.

        Returns:
            None
        """
        if new_capacity < 1:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        old_buckets = self._buckets
        self._buckets = new_buckets
        old_capacity = self._capacity
        self._capacity = new_capacity
        self._size = 0

        for idx in range(old_capacity):
            current_bucket = old_buckets[idx]
            if current_bucket is not None and not current_bucket.is_tombstone:
                self.put(current_bucket.key, current_bucket.value)

    def get(self, key: str) -> object:
        """
        Description:
            Method takes a passed key value and returns the associated value
            that's currently stored in the hash map. If the key is not in the
            hash map, the method returns None.

        Parameters:
            key: passed key value to locate associated value stored in hash
            map.

        Returns:
            value: value in hash map associated with passed key, or None if
            key is not found.
        """
        index = self._hash_function(key) % self._capacity
        original_index = index
        i = 1
        while self._buckets[index] is not None:
            if (not self._buckets[index].is_tombstone and
                    self._buckets[index].key == key):
                return self._buckets[index].value
            index = (original_index + i ** 2) % self._capacity
            i += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Description:
            Method takes a key value as a parameter and checks if the key is
            already in the hash map. If the key is already in the hash map,
            it returns True. Otherwise, it returns False; including if the
            hash map is empty (i.e. no keys included).

        Parameters:
            key: passed key value to check if in hash map.

        Returns:
            True if the key is in the hash map, False otherwise.
        """
        index = self._hash_function(key) % self._capacity
        original_index = index
        i = 1
        while self._buckets[index] is not None:
            if (not self._buckets[index].is_tombstone and
                    self._buckets[index].key == key):
                return True
            index = (original_index + i ** 2) % self._capacity
            i += 1
        return False

    def remove(self, key: str) -> None:
        """
        Description:
            Method takes a passed key value and removes the key/value pair
            currently stored in the hash map. If the key is not in the hash
            map, nothing happens (no exceptions raised).

        Parameters:
            key: passed key value to locate associated value stored in hash
            map.

        Returns:
            None
        """
        index = self._hash_function(key) % self._capacity
        original_index = index
        i = 1
        while self._buckets[index] is not None:
            if (not self._buckets[index].is_tombstone and
                    self._buckets[index].key == key):
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return
            index = (original_index + i ** 2) % self._capacity
            i += 1

    def clear(self) -> None:
        """
        Description:
            Method takes no parameters and clears the contents of the hash map.
            It doesn't alter the current hash table capacity.

        Parameters:
            None

        Returns:
            None
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Description:
            Method takes no parameters and returns a Dynamic Array of all the
            keys and values stored in the hash map. The returned Dynamic
            Array does not have any specified order or sorting.

        Parameters:
            None

        Returns:
            keys_values: Dynamic Array of the keys and values in the hash map.
            Not ordered or sorted.
        """
        keys_values = DynamicArray()
        for idx in range(self._capacity):
            entry = self._buckets[idx]
            if entry is not None and not entry.is_tombstone:
                keys_values.append((entry.key, entry.value))
        return keys_values

    def __iter__(self):
        """
        Description:
            This iterates through the hash map.
        Parameter:
            None
        Returns:
            self
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Description:
            This method returns the next item in the hash map based on the
            current location of the iterator.
        Parameter:
            None
        Returns:
            The next valid HashEntry in the hash map.
        """
        while self._index < self._capacity:
            entry = self._buckets[self._index]
            self._index += 1
            if entry is not None and not entry.is_tombstone:
                return entry
        raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
                  m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
                  m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'),
          m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'),
          m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to"
                  f"resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should"
                  f"be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(),
              round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))
    # #
    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
