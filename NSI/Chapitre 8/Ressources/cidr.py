from ip import *

def ad_reseau_cidr(ip_cidr1):
    """ Fonction qui renvoie l'adresse réseau """
    liste = ip_cidr1.split('/')
    ip1 = IP(liste[0])
    nb_1 = int(liste[1])
    chaine = ""
    octet = ""
    i = 0
    while i < 32:
        if i < nb_1:
            octet += "1"
        else:
            octet += "0"
        i += 1
        if i % 8 == 0 and i < 32:
            chaine += str(int(octet, 2)) + "."
            octet = ""
        if i == 32:
            chaine += str(int(octet, 2))
    masque = IP(chaine)
    return adresse_reseau(ip1, masque)
    
print(ad_reseau_cidr("192.168.145.12/24"))
print(ad_reseau_cidr("192.168.129.32/20"))
print(ad_reseau_cidr("192.198.127.19/23"))