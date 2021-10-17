from dico1 import entrer_dico

dico1 = entrer_dico('fichier1.csv', int)
dico1['Amaury'] = 16

print("Liste des personnes du dictionnaire ayant 17 ans :")
for nom, age in dico1.items():
    if age == 17:
        print(nom)
