# Name: Robert Smith
# OSU Email: Smithro8@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment: 6
# Due Date: 03/17/2023
# Description: A open addressing implementation of a hash table. Has various methods such as put, clear, get, and
#              contains.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
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
        Adds/updates a key and value. Overwrites if key exists
        If the load is 0.5 or greater it will resize to double its capacity
        """
        # resizes capacity if load 1+
        new_capacity = self._capacity * 2
        if self.table_load() >= .5:
            self.resize_table(new_capacity)
        # gets index
        index, size = self.get_hash_index(key)
        self._size += size
        self._buckets[index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the current table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes to the passed capacity
        Rehashes the keys after resize
        Will not make it smaller than the current size
        Makes sure the new capacity is prime
        otherwise gets the next prime value greater than the passed capacity
        """
        # if less than 1
        if new_capacity < self._size:
            return
        else:
            temp_hash = self._buckets
            # finds new capacity
            if self._is_prime(new_capacity):
                self._capacity = new_capacity
            else:
                new_capacity = self._next_prime(new_capacity)
                self._capacity = new_capacity
            # clears old hash
            self.clear()
            # rehashes
            for index in range(temp_hash.length()):
                if temp_hash[index] is not None and temp_hash[index].is_tombstone is False:
                    self.put(temp_hash[index].key, temp_hash[index].value)

    def get(self, key: str) -> object:
        """
        Returns the value of the passed key
        Otherwise returns none if not in hash
        """
        index, size = self.get_hash_index(key, 1)
        if self._buckets[index] is not None:
            return self._buckets[index].value
        return

    def contains_key(self, key: str) -> bool:
        """
        Returns True if in hash
        Otherwise False
        """
        index, size = self.get_hash_index(key)
        if self._buckets[index] is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """
        Removes the given key and value by making tombstone True
        If the key does not exist it does nothing
        """
        index, size = self.get_hash_index(key, 1)
        if self._buckets[index] is None:
            return
        self._buckets[index].is_tombstone = True
        self._size -= 1
        return

    def clear(self) -> None:
        """
        Clears the current hash table
        """
        self._buckets = DynamicArray()
        for x in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array of the keys and values as a tuple in the DA
        """
        dynamic_array = DynamicArray()
        for index in range(self._capacity):
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                tup = self._buckets[index].key, self._buckets[index].value
                dynamic_array.append(tup)
        return dynamic_array

    def __iter__(self):
        """
        Creates iterator and number of returned values for loop
        """
        self._index = 0
        self._returned_vals = 0
        return self

    def __next__(self):
        """
        Gets the next valid object and advances iterator
        """
        try:
            conditional = 0
            # stops iteration once all vals returned
            if self._returned_vals == self._size:
                conditional = 1
            while conditional == 0:
                # iterates to next non-none object
                if self._buckets[self._index] is None:
                    while self._buckets[self._index] is None:
                        self._index += 1
                # iterates past tombstoned objects
                if self._buckets[self._index] is not None:
                    if self._buckets[self._index].is_tombstone is False:
                        conditional = 1
                    if self._buckets[self._index].is_tombstone is True:
                        while self._buckets[self._index].is_tombstone is True:
                            self._index += 1
            value = self._buckets[self._index]
            self._index += 1
            # raises StopIteration
            if value is None:
                raise DynamicArrayException
            if value is not None:
                if value.is_tombstone is True:
                    raise DynamicArrayException
            self._returned_vals += 1
            return value
        except DynamicArrayException:
            raise StopIteration

    def get_hash_index(self, key, remove=0):
        """
        Returns the hash index
        """
        # gets first hash index
        hash = self._hash_function(key)
        index = hash % self._capacity

        # quadratic probing if not empty
        size = 0
        probe = 1
        conditional = 0
        spots = None
        initial_index = index
        while self._buckets[index] is not None:
            # if index was removed, index open
            # passes if looking for value to remove since key will match
            if remove == 0:
                if self._buckets[index].is_tombstone is True:
                    return index, size
            if self._buckets[index].key == key and \
                    self._buckets[index].is_tombstone is False:
                size = -1
                return index, size
            if conditional == 0:
                index = initial_index + probe ** 2
            if index >= self._capacity:
                conditional += 1
                spots = self._capacity
            if conditional > 0:
                index = (initial_index + probe ** 2) % spots
            probe += 1

        return index, size


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
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
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
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
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
    m.remove('2')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
