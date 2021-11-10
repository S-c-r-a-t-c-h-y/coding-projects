from liste_chainee import Liste_chainee
import math
import numpy as np
import time


class HashTable:
    def __init__(self, modulo=2 ** 16):
        self.__values = np.full((modulo,), Liste_chainee())
        self.__modulo = modulo

    def hash(self, elem):
        code = sum(math.pi * ord(lettre) * (256 ** i) for i, lettre in enumerate(elem))
        code = math.floor(code)
        return code % self.__modulo

    def __contains__(self, key):
        hash = self.hash(key)
        head = self.__values[hash].get_tete()
        while head is not None:
            if head.get_valeur()[0] == key:
                return True
            head = head.get_suivant()
        return False

    def __getitem__(self, key):
        if key not in self:
            return KeyError("Key not in hash table")
        hash = self.hash(key)
        head = self.__values[hash].get_tete()
        while head.get_valeur()[0] != key:
            head = head.get_suivant()
        return head.get_valeur()[1]

    def __setitem__(self, key, value):
        hash = self.hash(key)
        self.__values[hash].placer((key, value))

    def __delitem__(self, key):
        if key not in self:
            return KeyError("Key not found in hash table")
        hash = self.hash(key)
        head = self.__values[hash].get_tete()
        while head.get_valeur()[0] != key:
            head = head.get_suivant()
        head = None


table = HashTable()

# table["moi"] = 16
# table["leny"] = 16
# table["alois"] = 17

# table["FEDS"] = 20
# table["SOCK"] = 30

# print("moi" in table)
# print("toi" in table)

# print("FEDS" in table)
# print("SOCK" in table)

# print(table["leny"])
# print(table["FEDS"])
# print(table["SOCK"])


# def hacher(elem):
#     code = sum(math.pi * ord(lettre) * (256 ** i) for i, lettre in enumerate(elem))
#     code = math.floor(code)
#     return code % (2 ** 16)


with open("hachage.txt", "r", encoding="utf-8") as f:
    text = f.read()


for word in text.split():
    table[word] = 0

d = {str(i): 0 for i in range(50000)}
start = time.time()

for _ in range(1000):
    # a = "FEDS" in table
    a = "14599" in d

t = time.time() - start
print(f"{t:.10f}")


# coeff = sorted([len(valeur) for valeur in dico.values()])
# print(coeff, "\n")
# print({diff: coeff.count(diff) for diff in set(coeff)})
# print(max_hash)
