from math import sqrt


def factors(n):
    factors = set()
    i = 1
    while i <= sqrt(n):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
        i += 1

    return factors


def triangle_numbers():
    n = 1
    sum = 1
    while True:
        yield sum
        n += 1
        sum += n


for i in triangle_numbers():
    if len(factors(i)) > 500:
        print(i)
        break
