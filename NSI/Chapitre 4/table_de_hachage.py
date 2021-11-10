import math
import numpy as np
import time


class Pair:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def empty(self):
        return self.key is None and self.value is None


class HashTable:
    def __init__(self, size=100000):
        self.__values = np.full((size,), Pair())  # numpy array full of empty pairs
        self.__size = size

    def hash(self, elem):
        """Hashing function"""
        code = sum(math.pi * ord(lettre) * (256 ** i) for i, lettre in enumerate(elem))
        code = math.floor(code)
        return code

    def __contains__(self, key):
        hash = self.hash(key)
        for i in range(len(self.__values)):
            j = (hash + i) % self.__size
            if self.__values[j].empty():
                return False
            elif self.__values[j].key == key:
                return True

        return False

    def __getitem__(self, key):
        hash = self.hash(key)
        for i in range(len(self.__values)):
            j = (hash + i) % self.__size
            if self.__values[j].empty():
                raise KeyError(key)
            elif self.__values[j].key == key:
                return self.__values[j].value

        raise KeyError(key)

    def __setitem__(self, key, value):
        hash = self.hash(key)
        for i in range(len(self.__values)):
            j = (hash + i) % self.__size
            if self.__values[j].empty():
                self.__values[j] = Pair(key, value)
                return
            elif self.__values[j].key == key:
                self.__values[j].value = value

        raise MemoryError("No space remaining in hash table.")

    def __delitem__(self, key):
        hash = self.hash(key)
        for i in range(len(self.__values)):
            j = (hash + i) % self.__size
            if self.__values[j].empty():
                raise KeyError(key)
            elif self.__values[j].key == key:
                self.__values[j].value = Pair()

        raise KeyError(key)

    def __len__(self):
        return [not (elem.empty()) for elem in self.__values].count(True)

    # ! voir http://cermics.enpc.fr/polys/oap/node59.html pour plus de détail


table = HashTable()

### Table de hachage avec environ 500000 mots ###
#################################################

with open("hachage.txt", "r", encoding="utf-8") as f:
    text = f.read()

for word in text.split():
    table[word] = 0

### Temps d'execution pour 10000 tests d'appartenance dans la table de hachage ###
##################################################################################

start = time.time()

for _ in range(10000):
    a = "FEDS" in table

t = time.time() - start
print(f"{t:.10f}")

### Temps d'execution pour 10000 tests d'appartenance dans le dictionnaire python ###
##################################################################################

d = {str(i): i for i in range(50000)}

start = time.time()

for _ in range(10000):
    a = "14599" in d

t = time.time() - start
print(f"{t:.10f}")
