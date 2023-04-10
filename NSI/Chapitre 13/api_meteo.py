import requests
import matplotlib.pyplot as plt
from PIL import Image

# documentation sur l'api
# https://www.prevision-meteo.ch/uploads/pdf/recuperation-donnees-meteo.pdf

# liste des villes
# https://www.prevision-meteo.ch/services/json/list-cities

# url de l'api pour la ville d'Evian
ville = "Evian-les-bains"
url = "http://www.prevision-meteo.ch/services/json/" + ville

# recupere la page obtenu après la requette GET
reponse = requests.get(url)

# transforme le fichier reponse du format json en dictionnaire
dico_reponse = reponse.json()


def test1():
    # Affichage des différentes clés du dictionnaire dico_reponse
    print("** dico reponse **")
    for cle in dico_reponse:
        print(cle)
    print()


def test2():
    # Affichage des différentes clés du dictionnaire current_condition inclus dans le dictionnaire dico_reponse
    print("** dico conditions actuelles **")
    for cle in dico_reponse["fcst_day_0"]["hourly_data"]:
        print(cle)
        print(dico_reponse["fcst_day_0"]["hourly_data"][cle]["TMP2m"])
    print()


def test3():
    # Affiche la valeur de la clé condition du dictionnaire current_condition
    print("** condition **")
    print(dico_reponse["current_condition"]["condition"])
    print()


def test4():
    # Recupération de l'image qui est la valeur de la clé icon du dictionnaire current_condition
    print("icone")
    url_png = dico_reponse["current_condition"]["icon"]
    im = Image.open(requests.get(url_png, stream=True).raw)
    im.show()


def TP1():
    print(f"température actuelle : {dico_reponse['current_condition']['tmp']}")


def TP2():
    print(f"heure du lever du soleil : {dico_reponse['city_info']['sunrise']}")
    print(f"heure du coucher du soleil : {dico_reponse['city_info']['sunset']}")


def TP3():
    liste_heure = list(range(24))
    liste_tmp = []
    for cle in dico_reponse["fcst_day_0"]["hourly_data"]:
        liste_tmp.append(dico_reponse["fcst_day_0"]["hourly_data"][cle]["TMP2m"])

    plt.xlabel("heures")
    plt.ylabel("températures en °C")
    plt.title("Prévision ds températures aujourd'hui à Evian")

    plt.scatter(liste_heure, liste_tmp)
    plt.plot(liste_heure, liste_tmp)

    plt.show()


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    # test4()
    # TP1()
    # TP2()
    TP3()
    pass
