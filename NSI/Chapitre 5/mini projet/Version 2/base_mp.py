#!/usr/bin/python

import sqlite3
from sqlite3 import Error


def creer_connexion(db_file):
    """cree une connexion a la base de donnees SQLite
        specifiee par db_file
    :param db_file: fichier BD
    :return: objet connexion ou None
    """
    try:
        conn = sqlite3.connect(db_file)
        # On active les foreign keys
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except Error as e:
        print(e)

    return None


def select_toutes_classes(conn):
    """
    :param conn: objet connexion
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Classe")

    rows = cur.fetchall()

    print("Liste de toutes les classes :")
    for row in rows:
        print(row)


def select_tous_élèves(conn):
    cur = conn.cursor()
    cur.execute("SELECT Nom, Prenom, IDClasse FROM Eleve JOIN Personne ON Eleve.IDPersonne = Personne.IDPersonne")

    rows = cur.fetchall()

    print("Liste de tout les élèves :")
    for row in rows:
        print(row)


def eleves_prenom(conn, nom):
    cur = conn.cursor()
    cur.execute(f"SELECT Prenom FROM Personne JOIN Eleve ON Personne.IDPersonne=Eleve.IDPersonne WHERE Nom='{nom}'")

    rows = cur.fetchall()

    if rows:
        print("Elèves avec ce nom : ")
        for row in rows:
            print(row[0])
    else:
        print(f"Aucun élèves n'ont le nom {nom}.")


def eleve_in(conn, nom, prenom):
    cur = conn.cursor()
    cur.execute(
        f"SELECT Nom, Prenom FROM Personne JOIN Eleve ON Eleve.IDPersonne = Personne.IDPersonne WHERE Nom='{nom}' AND Prenom='{prenom}'"
    )

    rows = cur.fetchall()

    return bool(rows)


def classe_eleve(conn, nom, prenom):
    cur = conn.cursor()
    cur.execute(
        f"SELECT Classe.nom FROM Classe JOIN Eleve ON Classe.IDClasse=Eleve.IDClasse JOIN Personne ON Eleve.IDPersonne = Personne.IDPersonne WHERE Personne.Nom='{nom}' AND Personne.Prenom='{prenom}'"
    )

    rows = cur.fetchall()

    if rows:
        print("Classe de l'élève :")
        print(rows[0][0])
    elif not (eleve_in(conn, nom, prenom)):
        print("L'élève n'est pas dans l'établissement")
    else:
        print("L'élève n'est dans aucune classe")


def nb_eleves_classe(conn, nom_classe):
    cur = conn.cursor()
    cur.execute(
        f"SELECT COUNT(*) FROM Eleve JOIN Classe ON Classe.IDClasse=Eleve.IDClasse WHERE Classe.Nom='{nom_classe}'"
    )

    rows = cur.fetchall()

    print("Nombre d'élèves dans la classe :")
    for row in rows:
        print(row[0])


def matiere(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Matiere FROM Cours")

    rows = cur.fetchall()

    print("Matières présentes dans l'établissement : ")
    for row in rows:
        print(row[0])


def cursus_eleve(conn, nom, prenom):
    cur = conn.cursor()

    if not eleve_in(conn, nom, prenom):
        print("Cet élève ne fait pas partie de l'établissement.")
        return

    cur.execute(
        f"SELECT DISTINCT Matiere FROM Cours JOIN Cursus ON Cours.IDCours = Cursus.IDCours JOIN Eleve ON Cursus.IDEleve = Eleve.IDEleve JOIN Personne ON Personne.IDPersonne = Eleve.IDPersonne WHERE Personne.Nom = '{nom}' AND Personne.Prenom = '{prenom}'"
    )

    rows = cur.fetchall()

    if rows:
        rep = "Matières de l'élève : "
        for row in rows:
            rep += row[0]
            rep += ", "
        print(rep[:-1])
    else:
        print("Cet élève fais partie de l'établissement, mais ne suit pas de cours.")


def eleves_cours(conn, IDCours):
    cur = conn.cursor()
    cur.execute(
        f"SELECT Personne.Nom, Personne.Prenom FROM Personne JOIN Eleve ON Eleve.IDPersonne = Personne.IDPersonne JOIN Cursus ON Cursus.IDEleve = Eleve.IDEleve WHERE Cursus.IDCours = '{IDCours}'"
    )

    rows = cur.fetchall()

    if rows:
        print("Elèves qui suivent ce cours :")
        for row in rows:
            print(row)
    else:
        print("Personne ne suit ce cours / aucun cours ne correspond à cet ID.")


def nb_eleves_cours(conn, IDCours):
    cur = conn.cursor()
    cur.execute(
        f"SELECT COUNT(*) FROM Eleve JOIN Cursus ON Cursus.IDEleve = Eleve.IDEleve WHERE Cursus.IDCours = '{IDCours}'"
    )

    rows = cur.fetchall()

    print("Nombre d'élèves dans ce cours :")
    for row in rows:
        print(row[0])


def eleves_professeur(conn, nom, prenom):
    cur = conn.cursor()
    cur.execute(
        f"SELECT Personne.Nom, Personne.Prenom FROM Personne JOIN Eleve ON Personne.IDPersonne = Eleve.IDPersonne JOIN Cursus ON Eleve.IDEleve = Cursus.IDEleve JOIN Cours ON Cours.IDCours = Cursus.IDCours JOIN Professeur ON Cours.IDProfesseur = Professeur.IDProfesseur JOIN Personne AS p ON p.IDPersonne = Professeur.IDPersonne WHERE p.Nom = '{nom}' AND p.Prenom = '{prenom}'"
    )

    rows = cur.fetchall()

    print("Eleves ayant ce professeur en cours :")
    for row in rows:
        print(row)


def majBD(conn, file):

    # Lecture du fichier et placement des requetes dans un tableau
    createFile = open(file, "r")
    createSql = createFile.read()
    createFile.close()
    sqlQueries = createSql.split(";")

    # Execution de toutes les requetes du tableau
    cursor = conn.cursor()
    for query in sqlQueries:
        # print(query)
        cursor.execute(query)

    # commit des modifications
    conn.commit()


def main():
    database = "base_mp.db"

    # creer une connexion a la BD
    conn = creer_connexion(database)

    # remplir la BD
    print("1. On cree les tables et on les initialise avec des premieres valeurs.")
    majBD(conn, "base_mp.sql")

    # Menu
    continuer = True
    while continuer:
        print("\n MENU")
        print("1 : Terminer")
        print("2 : Afficher la liste de toutes les classes")
        print("3 : Afficher la liste de tous les élèves")
        print("4 : Afficher la liste de tous les prénoms des élèves avec un certain nom")
        print("5 : Vérifie si un certain élève est dans l'établissement")
        print("6 : Affiche la classe d'un certain élève")
        print("7 : Affiche le nombre d'élèves dans un certaine classe")
        print("8 : Affiche les élèves ayant un certain professeur en cours")
        print("9 : Exemples étape 2")

        choix = int(input())
        if choix == 1:
            continuer = False

        elif choix == 2:
            # lire la BD
            select_toutes_classes(conn)

        elif choix == 3:
            # lire la BD
            select_tous_élèves(conn)

        elif choix == 4:
            # lire la BD
            nom = input("Nom de famille : ")
            eleves_prenom(conn, nom)

        elif choix == 5:
            nom = input("Nom de famille de l'élève : ")
            prenom = input("Prénom de l'élève : ")

            if eleve_in(conn, nom, prenom):
                print(f"{nom} {prenom} est dan l'établissement")
            else:
                print(f"{nom} {prenom} n'est pas élève dans l'établissement")

        elif choix == 6:
            nom = input("Nom de famille de l'élève : ")
            prenom = input("Prénom de l'élève : ")

            classe_eleve(conn, nom, prenom)

        elif choix == 7:
            classe = input("Nom de la classe : ")

            nb_eleves_classe(conn, classe)

        elif choix == 8:
            nom = input("Nom de famille du professeur : ")
            prenom = input("Prénom du professeur : ")

            eleves_professeur(conn, nom, prenom)

        elif choix == 9:
            test(conn)

    # commit des modifications eventuelles
    conn.commit()

    # fermeture de la connexion
    conn.close()


def test(conn):
    print("####################")
    print("Test de la fonction cursus_eleve pour Bourgeois Michel")
    cursus_eleve(conn, "Bourgeois", "Michel")
    print("####################")
    print("Test fonction cursus_eleve pour Brel Jacqueline")
    cursus_eleve(conn, "Brel", "Jacqueline")
    print("####################")
    print("Test fonction cursus_eleve pour Marchal Dimitri")
    cursus_eleve(conn, "Marchal", "Dimitri")
    print("####################")
    print("Test de la fonction nb_eleves_cours")
    nb_eleves_cours(conn, 5)
    print("####################")
    print("Test de la fonction eleves_cours")
    eleves_cours(conn, 4)


if __name__ == "__main__":
    main()
