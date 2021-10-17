from dico1 import entrer_dico

dico_scrabble = entrer_dico('scrabble.csv', int)

def point(mot):
    points = 0
    for lettre in mot:
        points += dico_scrabble[lettre]
    return points

print(point('BON'))
print(point('ZOO'))
print(point('ZIZANIE'))