import tkinter as tk
import time
import math


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.width = 800
        self.height = 500

        self.geometry(f"{self.width}x{self.height}")
        self.title("Bonhomme qui travaille philo")
        self.configure(background="white")
        self.resizable(width=False, height=False)

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.taille_caisse = 100

        self.caisses = [
            self.creer_caisse(500, self.height - self.taille_caisse, self.taille_caisse, self.taille_caisse),
            self.creer_caisse(600, self.height - self.taille_caisse, self.taille_caisse, self.taille_caisse),
            self.creer_caisse(700, self.height - self.taille_caisse, self.taille_caisse, self.taille_caisse),
            self.creer_caisse(550, self.height - 2 * self.taille_caisse, self.taille_caisse, self.taille_caisse),
            self.creer_caisse(650, self.height - 2 * self.taille_caisse, self.taille_caisse, self.taille_caisse),
            self.creer_caisse(600, self.height - 3 * self.taille_caisse, self.taille_caisse, self.taille_caisse),
        ]
        self.index_caisse = 0

        self.fleche = self.canvas.create_line(300, self.height / 2, 450, self.height / 2, fill="red", width=5)
        self.fleche = self.canvas.create_line(420, self.height / 2 - 20, 450, self.height / 2, fill="red", width=5)
        self.fleche = self.canvas.create_line(420, self.height / 2 + 20, 450, self.height / 2, fill="red", width=5)

        self.text = self.canvas.create_text(
            365, self.height / 2 + 10, text="énergie\ncompétence\ntemps", font=("Helvetica", "15", "bold")
        )

        self.titre = self.canvas.create_text(
            400, 30, text="les effets de l'alinéation sur l'ouvrier", font=("Helvetica", "20", "bold")
        )

        self.chaussure_gauche = self.canvas.create_rectangle(
            50, self.height - 30, 100, self.height, fill="gray", outline="white"
        )
        self.chaussure_droite = self.canvas.create_rectangle(
            150, self.height - 30, 200, self.height, fill="gray", outline="white"
        )

        self.longueur_jambe = 120
        self.longueur_torse = 200
        self.hauteur_tete = 70

        self.dessiner_corps()
        self.dessiner_bras(-45)

        angle = -45
        sens = -1
        increment = len(self.caisses) + 1

        decrement_jambe = (self.longueur_jambe - 20) / (len(self.caisses) * 100)
        decrement_torse = (self.longueur_torse - 20) / (len(self.caisses) * 100)

        for i in range(len(self.caisses) * 100):

            if i % 100 == 0:
                self.apparaitre_caisse()
                increment -= 1
            if angle < -45 or angle > 45:
                sens *= -1
            angle += sens * increment

            self.longueur_jambe -= decrement_jambe
            self.longueur_torse -= decrement_torse

            self.canvas.delete(self.jambe_gauche)
            self.canvas.delete(self.jambe_droite)
            self.canvas.delete(self.corps)
            self.canvas.delete(self.tete)
            self.canvas.delete(self.bras_droit)
            self.canvas.delete(self.bras_gauche)

            self.dessiner_bras(angle)
            self.dessiner_corps()

            time.sleep(0.001)
            self.update()

        # self.canvas.delete(self.bras_droit)
        # self.canvas.delete(self.bras_gauche)

        self.mainloop()

    def rotate(self, points, angle, center):
        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = center
        new_points = []
        for x_old, y_old in points:
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new + cx, y_new + cy])
        return new_points

    def dessiner_corps(self):

        self.jambe_gauche = self.canvas.create_rectangle(
            70, self.height - 30, 100, self.height - 30 - self.longueur_jambe, fill="navy", outline="white"
        )
        self.jambe_droite = self.canvas.create_rectangle(
            150, self.height - 30, 180, self.height - 30 - self.longueur_jambe, fill="navy", outline="white"
        )

        self.corps = self.canvas.create_rectangle(
            70,
            self.height - 30 - self.longueur_jambe,
            180,
            self.height - 30 - self.longueur_jambe - self.longueur_torse,
            fill="black",
            outline="white",
        )

        self.tete = self.canvas.create_oval(
            90,
            self.height - 30 - self.longueur_jambe - self.longueur_torse,
            160,
            self.height - 30 - self.longueur_jambe - self.longueur_torse - self.hauteur_tete,
            fill="PeachPuff3",
            outline="white",
        )

    def dessiner_bras(self, angle):

        # brase droit
        points = [
            (180, self.height - 30 - self.longueur_jambe - self.longueur_torse + 10),
            (280, self.height - 30 - self.longueur_jambe - self.longueur_torse + 10),
            (280, self.height - 30 - self.longueur_jambe - self.longueur_torse + 30),
            (180, self.height - 30 - self.longueur_jambe - self.longueur_torse + 30),
        ]
        points = self.rotate(points, angle, (180, self.height - 30 - self.longueur_jambe - self.longueur_torse + 10))
        self.bras_droit = self.canvas.create_polygon(points, fill="black", outline="white")

        points = [
            (70, self.height - 30 - self.longueur_jambe - self.longueur_torse + 10),
            (-30, self.height - 30 - self.longueur_jambe - self.longueur_torse + 10),
            (-30, self.height - 30 - self.longueur_jambe - self.longueur_torse + 30),
            (70, self.height - 30 - self.longueur_jambe - self.longueur_torse + 30),
        ]
        points = self.rotate(points, -angle, (70, self.height - 30 - self.longueur_jambe - self.longueur_torse + 10))
        self.bras_gauche = self.canvas.create_polygon(points, fill="black", outline="white")

    def creer_caisse(self, x, y, taille_x, taille_y):
        return self.canvas.create_rectangle(x, y, x + taille_x, y + taille_y, fill="white", outline="white")

    def apparaitre_caisse(self):
        self.canvas.itemconfigure(self.caisses[self.index_caisse], fill="#6e472d", outline="black")
        self.index_caisse = self.index_caisse + 1 if self.index_caisse != len(self.caisses) - 1 else 0


app = App()
