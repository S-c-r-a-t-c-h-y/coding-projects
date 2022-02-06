class IP:
    """ Classe modélisant une adresse IPv4"""
    # Constructeur
    def __init__(self, chaine):
        self.liste = [int(n) for n in chaine.split('.')]
    # Surcharge de la fonction print
    def __repr__(self):
        """ Surcharge de la fonction print() """
        chaine = str(self.liste[0])
        for e in self.liste[1:]:
            chaine += '.' + str(e)
        return chaine
    
def adresse_reseau(ip1, masque):
    """ Fonction qui retourne l'adresse du réseau """
    chaine = ""
    for i in range(4):
        chaine += str(ip1.liste[i] & masque.liste[i]) + "."
    ad_reseau = IP(chaine[:-1])
    return ad_reseau

if __name__ == "__main__":
    ip1 = IP("192.168.137.11")
    masque = IP("255.255.240.0")
    print(adresse_reseau(ip1, masque))

    ip1 = IP("192.208.127.19")
    masque = IP("255.255.224.0")
    print(adresse_reseau(ip1, masque))

    ip1 = IP("178.105.186.27")
    masque = IP("255.255.128.0")
    print(adresse_reseau(ip1, masque))
