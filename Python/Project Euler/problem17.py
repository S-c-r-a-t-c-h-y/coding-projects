def unit_number(n):
    return n % 10


def dozen_number(n):
    return (n % 100) // 10


def hundreds_number(n):
    return (n % 1000) // 100


nb_letters = {
    0: 0,
    1: 3,
    2: 3,
    3: 5,
    4: 4,
    5: 4,
    6: 3,
    7: 5,
    8: 5,
    9: 4,
    10: 3,
    11: 6,
    12: 6,
    13: 8,
    14: 8,
    15: 7,
    16: 7,
    17: 9,
    18: 8,
    19: 8,
    20: 6,
    30: 6,
    40: 5,
    50: 5,
    60: 5,
    70: 7,
    80: 6,
    90: 6,
}


def letter_amt(n):
    sum = 0
    if n == 1000:
        return 11
    elif n % 100 <= 19:
        sum += nb_letters[n % 100]
    else:
        sum += nb_letters[unit_number(n)]
        sum += nb_letters[dozen_number(n) * 10]
    if n >= 100:
        sum += nb_letters[hundreds_number(n)]
        sum += 7
        if n % 100 != 0:
            sum += 3
    return sum


print(sum(letter_amt(i) for i in range(1, 1001)))
