
a = "cherche youtube sur google".split(" ")
b = "cherche sur google".split(" ")

commande = ""
if 'cherche' in a and 'sur' in a and 'google' in a and a != b:
    for elem in a:
        if elem not in b:
            commande += f"{elem} "
    commande = commande[:-1]
            
print(commande)