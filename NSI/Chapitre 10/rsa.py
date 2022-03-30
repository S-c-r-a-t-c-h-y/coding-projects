# https://www.gaudry.be/crypto-rsa.html

import math
import random


def random_prime(min_prime=0, max_prime=1000):
    def is_prime(n):
        return False if n < 2 else all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))

    return random.choice([i for i in range(min_prime, max_prime + 1) if is_prime(i)])


def pgcd(a, b):
    return max(a, b) if 0 in {a, b} else pgcd(b, a % b)


def eucl(a, b):
    if b == 0:
        return a, 1, 0
    d, u, v = eucl(b, a % b)
    return d, v, u - (a // b) * v


def mod_inverse(x, m):
    return eucl(x, m)[1] % m


def phi(p, q):
    return (p - 1) * (q - 1)


def generate_random_rsa(prime_min: int = 100, prime_max: int = 1000):
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


# --------------------------------------------------------------------------------------------------


def puissance_mod(m, e, n):
    """Fonction qui retourne le calcul de m**e % n"""
    return (m ** e) % n


def chiffrer_rsa(texte, e, n):
    """Fonction qui chiffre chaque caractère du texte à partir de son code ASCII
    en appliquant la clé publique (e, n) du code RSA et qui retourne une chaîne
    constituée des codes séparés par des espaces.
    """
    return " ".join(str(puissance_mod(ord(car), e, n)) for car in texte)


def dechiffrer_rsa(texte, d, n):
    """Fonction qui déchiffre un texte crypté en code RSA en texte clair
    en utilisant la clé privée (d, n)
    """
    return "".join(chr(puissance_mod(int(car), d, n)) for car in texte.split(" "))


if __name__ == "__main__":
    # print(puissance_mod(80, 43, 527))
    # print(puissance_mod(65, 43, 527))
    # print(puissance_mod(82, 43, 527))
    # print(puissance_mod(67, 43, 527))
    # print()
    # print(puissance_mod(516, 67, 527))
    # print(puissance_mod(520, 67, 527))
    # print(puissance_mod(10, 67, 527))
    # print(puissance_mod(67, 67, 527))

    print(chiffrer_rsa("PARC", 43, 527))
    print(chiffrer_rsa("LAC", 43, 527))
    # print(chiffrer_rsa("BAC", 43, 527))
    print()
    print(dechiffrer_rsa("121 520 67", 67, 527))
    print(dechiffrer_rsa("516 520 10 67", 67, 527))
