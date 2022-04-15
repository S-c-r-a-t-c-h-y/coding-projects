# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import requests

# Récupération de la liste de toutes les villes dont la météo est disponible
def liste_villes():
    url = "https://www.prevision-meteo.ch/services/json/list-cities"

    response = requests.get(url)
    data = response.json()

    return [ville["url"] for ville in list(data.values())]

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

liste_villes_valides = liste_villes()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", name="Jean")

@app.route("/meteo", methods=["GET", "POST"])
def meteo():
    nom_ville = str(request.args.get("ville"))
    
    if nom_ville in liste_villes_valides:
        ville, cond, tmp, img_url = obtenir_infos(nom_ville)
        return render_template("page_meteo.html", ville=ville, cond=cond.lower(), tmp=tmp, img_url=img_url)
    
    return render_template("page_erreur.html")

if __name__ == "__main__":
    app.run()
