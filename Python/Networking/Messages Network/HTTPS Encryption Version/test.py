import math
import random
from typing import Tuple


def generate_random_rsa(prime_min: int = 100, prime_max: int = 1000) -> Tuple[int, int, int]:
    """generates a random rsa key pair (e, d, n)"""

    def random_prime(min_prime=0, max_prime=1000):
        def is_prime(n):
            return False if n < 2 else all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))

        return random.choice([i for i in range(min_prime, max_prime + 1) if is_prime(i)])

    def pgcd(a, b):
        return max(a, b) if 0 in {a, b} else pgcd(b, a % b)

    def mod_inverse(x, m):
        def eucl(a, b):
            if b == 0:
                return a, 1, 0
            d, u, v = eucl(b, a % b)
            return d, v, u - (a // b) * v

        return eucl(x, m)[1] % m

    def phi(p, q):
        return (p - 1) * (q - 1)

    d = e = n = 1

    while (((1000 ** e) % n) ** d) % n != 1000:
        p, q = random_prime(prime_min, prime_max), random_prime(prime_min, prime_max)

        n = p * q
        phi_n = phi(p, q)

        for i in range(max(p, q) + 1, phi_n):
            if pgcd(i, phi_n) == 1:
                e = i
                break

        d = mod_inverse(e, phi_n)
    return e, d, n


e, d, n = generate_random_rsa()
print(e, d, n)
