from sys import setrecursionlimit

setrecursionlimit(100000)

values = {}


def fib(n):
    if n <= 1:
        return 1
    if n in values:
        return values[n]
    res = fib(n - 1) + fib(n - 2)
    values[n] = res
    return res


n = 1
while len(str(fib(n))) < 1000:
    n += 1

print(n, fib(n))
