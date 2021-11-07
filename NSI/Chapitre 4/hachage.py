
def hacher(mot):
    code = 0
    for i, lettre in enumerate(mot):
        code += (ord(lettre) * (256 ** i))
    return code % (2**64)

with open("hachage.txt", "r", encoding='utf-8') as f:
    text = f.read()

dico = {}

for word in text.split():
    hachage = hacher(word)
    if hachage in dico:
        dico[hachage].add(word)
    else:
        dico[hachage] = {word}

# print(dico)
coeff = sorted([len(valeur) for valeur in dico.values()])
print(coeff, "\n")
print({diff: coeff.count(diff) for diff in set(coeff)})