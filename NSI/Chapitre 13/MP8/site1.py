# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt

# Récupération de la liste de toutes les villes dont la météo est disponible
def liste_villes():
    url = "https://www.prevision-meteo.ch/services/json/list-cities"

    response = requests.get(url)
    data = response.json()

    return [{"url": ville["url"], "nom": ville["name"]} for ville in list(data.values())]

# Récupération des infos météo
def obtenir_infos(ville="Evian-les-bains"):
    url = f"http://www.prevision-meteo.ch/services/json/{ville}"

    response = requests.get(url)
    data = response.json()

    ville = data["city_info"]["name"]
    cond = data["current_condition"]["condition"]
    tmp = data["current_condition"]["tmp"]
    
    img_url = data["current_condition"]["icon"]
    
    return ville, cond, tmp, img_url

def creer_graphe_tmp(ville="Evian-les-bains"):
    url = f"http://www.prevision-meteo.ch/services/json/{ville}"

    response = requests.get(url)
    data = response.json()

    liste_heure = list(range(24))
    liste_tmp = [data["fcst_day_0"]["hourly_data"][cle]["TMP2m"] for cle in data["fcst_day_0"]["hourly_data"]]

    ville = data['city_info']['name']

    plt.clf()
    plt.xlabel("Heures")
    plt.ylabel("Températures en °C")
    plt.title(f"Prévision des températures aujourd'hui à {ville}")

    plt.scatter(liste_heure, liste_tmp)
    plt.savefig(f'./static/{ville}.png')
    

liste_villes = liste_villes()
liste_villes_valides = [ville["url"] for ville in liste_villes]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", liste_villes=liste_villes)

@app.route("/meteo", methods=["GET", "POST"])
def meteo():
    nom_ville = str(request.args.get("ville"))
    
    if nom_ville in liste_villes_valides:

        creer_graphe_tmp(nom_ville)
        ville, cond, tmp, img_url = obtenir_infos(nom_ville)
        return render_template("page_meteo.html", ville=ville, cond=cond.lower(), tmp=tmp, img_url=img_url)
    
    return render_template("page_erreur.html")

if __name__ == "__main__":
    app.run()
