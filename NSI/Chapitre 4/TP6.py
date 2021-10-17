from dico1 import entrer_dico

dico_morse = entrer_dico('morse.csv', str)

def morse(phrase):
    phrase = phrase.upper()
    rep = ''
    for lettre in phrase:
        rep += dico_morse[lettre]
        rep += ' '
    return rep

def inverser_dico(dico):
    return {valeur: cle for cle, valeur in dico.items()}

print(inverser_dico(dico_morse))
