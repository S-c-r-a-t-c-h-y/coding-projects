def pgcd(a, b):
    """Fonction récursive qui renvoie le pgcd de a et b"""
    if b == 0:
        return a
    return pgcd(b, a % b)

print('pgcd(18, 63) =', pgcd(18, 63))
print('pgcd(143, 221) =', pgcd(143, 221))
print('pgcd(31, 59) =', pgcd(31, 59))
print('pgcd(561, 1071) =', pgcd(561, 1071))