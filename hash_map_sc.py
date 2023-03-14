# Name: Robert Smith
# OSU Email: Smithro8@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment: 6
# Due Date: 03/17/2023
# Description: A chaining implementation of a hash table. Has various methods such as put, clear, get, and
#              contains.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
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
        Increment from given number and the find the closest prime number
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
        Adds the key/value pair in the hash map
        Replaces value if key exists
        Resizes if load table 1.0 or greater
        """
        # resizes capacity if load 1+
        new_capacity = self._capacity * 2
        if self.table_load() >= 1:
            self.resize_table(new_capacity)
        # gets index
        index = self.get_hash_index(key)
        # gets linked list at index
        link_list = self._buckets.get_at_index(index)
        # replaces value if key is already used
        if link_list.contains(key):
            link_list.remove(key)
            self._size -= 1
        # insert key/value
        link_list.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets
        """
        count = 0
        for index in range(self._capacity):
            link_list = self._buckets.get_at_index(index)
            if link_list.length() < 1:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Returns the hash's load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        """

        self._buckets = DynamicArray()
        for x in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the Hash Table, rehashes old values
        Makes sure new capacity is prime, else changes it to prime
        """
        # if less than 1
        if new_capacity < 1:
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
            for indexes in range(temp_hash.length()):
                linked_list = temp_hash[indexes]
                if linked_list.length() != 0:
                    for node in linked_list:
                        key, value = node.key, node.value
                        self.put(key, value)

    def get(self, key: str):
        """
        Gets the value associated with the key
        """
        index = self.get_hash_index(key)
        linked_list = self._buckets.get_at_index(index)
        node = linked_list.contains(key)
        if node is None:
            return
        return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if in hash
        Otherwise False
        """
        # if empty
        if self._size == 0:
            return False
        index = self.get_hash_index(key)
        linked_list = self._buckets.get_at_index(index)
        node = linked_list.contains(key)
        if node is None:
            return False
        if node.key == key:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and value by making tombstone True
        If the key does not exist it does nothing
        """
        # if empty
        if self._size == 0:
            return
        index = self.get_hash_index(key)
        linked_list = self._buckets.get_at_index(index)
        val = linked_list.remove(key)
        if val is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array of the keys and values as a tuple in the DA
        """
        da = DynamicArray()
        da_index = 0
        for indexes in range(self._capacity):
            linked_list = self._buckets.get_at_index(indexes)
            if linked_list.length() != 0:
                for nodes in linked_list:
                    tup = nodes.key, nodes.value
                    da.append(tup)
                    da_index += 1
        return da

    def get_hash_index(self, key) -> int:
        """
        Returns the hash index
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        return index


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a dynamic array and returns a dynamic array of the
    most occurring value(s) and a integer representing the frequency
    """
    # creates hash map
    map = HashMap(da.length())
    # sets element of da to map as keys and frequency as their value
    highest_frequency = 0
    for index in range(da.length()):
        key = da[index]
        value = map.get(key)
        # sets value to zero if value not in da
        if value is None:
            value = 0
        # inc value
        value += 1
        # sets highest frequency
        if value > highest_frequency:
            highest_frequency = value
        map.put(key, value)

    arr = DynamicArray()
    # appends most frequent vals to arr
    for index in range(da.length()):
        key = da[index]
        value = map.get(key)
        if value == highest_frequency:
            arr.append(key)
            map.remove(key)
    return arr, highest_frequency


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
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    print("\nPDF - resize example 2")
    print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(),
    #           round(m.table_load(), 2))
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
    m = HashMap(53, hash_function_1)
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
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())
    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())
    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu",
         "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )
    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
