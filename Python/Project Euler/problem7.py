from math import sqrt


def is_prime(n):
    divisor = 2

    while divisor <= sqrt(n):
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def prime_generator(amt):
    n = 2
    for _ in range(amt):
        while not is_prime(n):
            n += 1
        yield n
        n += 1


print(list(prime_generator(10001))[-1])
