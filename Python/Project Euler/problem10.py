from math import sqrt


def is_prime(n):
    divisor = 2

    while divisor <= sqrt(n):
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def prime_generator(treshold):
    n = 2
    while n < treshold:
        yield n
        n += 1
        while not is_prime(n):
            n += 1


print(sum(prime_generator(2_000_000)))
