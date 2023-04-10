# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template

# Nommage de l’application ici ce sera app
app = Flask(__name__)

# @app.route permet de préciser à quelle adresse ce qui suit va s’appliquer.
# la page suivante sera à la racine /
@app.route("/")

# Quand on arrive sur la page à la racinde du site "/" , on va en même temps appeler la fonction index().
def index():
    return f"<h1> Le super site </h1>  Ce site est construit à partir du framework Flask. <br> <a href = {url_for('p2')}> Lien vers la suite</a><br> <a href = {url_for('p3')}> Lien vers la troisieme page</a>"


# Quand on arrive sur la page à la racinde du site "/deuxieme" , on va en même temps appeler la fonction p2().
@app.route("/deuxieme")
def p2():
    return f"Nous sommes maintenant sur la deuxième page ! <br> <a href = {url_for('index')}> Lien vers l'index</a>"


@app.route("/troisieme")
def p3():
    return f"Nous sommes maintenant sur la troisième page ! <br> <a href = {url_for('index')}> Lien vers l'index</a>"


if __name__ == "__main__":
    # On lance l'application app si ce programme est lancé comme programme principal.
    app.run()
