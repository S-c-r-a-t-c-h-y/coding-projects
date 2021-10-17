from dico1 import entrer_dico

dico1 = entrer_dico('fichier1.csv', int)
dico1['Amaury'] = 16
for nom, age in dico1.items():
    print(f"{nom} a {age} ans.")