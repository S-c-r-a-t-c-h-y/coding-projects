def binaire(n):
    assert 0 <= n <= 255, "Le paramètre doit être compris entre 0 et 255."

    return str.rjust(bin(n)[2:], 8, "0")


def chiffrer_xor(texte, cle):
    return "".join(binaire(ord(car) ^ ord(cle[i % len(cle)])) for i, car in enumerate(texte))


def dechiffrer_xor(texte, cle):
    return "".join(chr(int(texte[i : i + 8], 2) ^ ord(cle[i // 8 % len(cle)])) for i in range(0, len(texte), 8))


if __name__ == "__main__":
    print(chiffrer_xor("BAC", "DE"))
    print(dechiffrer_xor("000001100000010000000111", "DE"))
    print(chiffrer_xor("PYTHON", "NSI"))

    print(chiffrer_xor("SALUT", "BAC"))
