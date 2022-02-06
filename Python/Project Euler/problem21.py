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


def d(n):
    divisors = list(factors(n))
    divisors.remove(n)
    return sum(divisors)


def is_amicable(a):
    b = d(a)
    if d(b) == a and a != b:
        return True


amicable_numbers = set()
for a in range(2, 10000):
    if is_amicable(a):
        amicable_numbers.add(a)
        amicable_numbers.add(d(a))

print(sum(amicable_numbers))
