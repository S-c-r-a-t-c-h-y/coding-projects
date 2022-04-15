# -*- coding: utf-8 -*-

from flask import Flask, render_template

# Nommage de l’application ici ce sera app
app = Flask(__name__)

# @app.route permet de préciser à quelle adresse ce qui suit va s’appliquer.
# la page suivante sera à la racine /
@app.route("/")
# Quand on arrive sur la page à la racinde du site "/" , on va en même temps appeler la fonction index().
def index():
    # On injecte dans le template (c'est un modèle) de la page index.html la variable name".
    return render_template("index.html", name="Jean")


# Quand on arrive sur la page à la racinde du site "/deuxieme/<nom>" , on va en même temps appeler la fonction p2(nom).
@app.route("/deuxieme/<nom>")
def p2(nom):
    # On injecte dans le template (c'est un modèle) deuxieme.html la variable name".
    return render_template("deuxieme.html", name=nom)


if __name__ == "__main__":
    # On lance l'application app si ce prograame est lancé comme programme principal.
    app.run()
