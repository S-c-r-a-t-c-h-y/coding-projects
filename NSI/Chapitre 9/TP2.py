import sys

sys.setrecursionlimit(10000)


def somme(n, c):
    if n == 0:
        print(f"{c + 1} opérations")
        return 0
    else:
        return n - 1 + somme(n - 1, c + 3)


print(somme(10, 0))
print(somme(20, 0))
print(somme(50, 0))
print(somme(100, 0))
print(somme(500, 0))
print(somme(1000, 0))
