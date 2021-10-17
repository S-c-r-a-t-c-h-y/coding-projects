def entrer_dico(nom_fichier, cast):
    """ Fontion qui entre le contenu d'un fichier CSV dans un dictionnaire dont
        les valeurs sont entières
    """
    import csv
    fichier = open(nom_fichier, encoding='utf-8')
    csv_en_liste = csv.reader(fichier)
    dict1 = {ligne[0]:cast(ligne[1]) for ligne in csv_en_liste}
    fichier.close()
    return dict1