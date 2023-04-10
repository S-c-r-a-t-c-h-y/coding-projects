import tkinter as tk
import tkinter.messagebox
import socket


class TicTacToe(tk.Tk):
    """Classe qui s'occupe de la création et du déroulement d'un jeu de morpion relié à un serveur"""

    win_conditions = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

    def __init__(self, player_nb):

        self.grid = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.turn = "x" if player_nb == "1" else "o"

        self.waiting = self.turn == "o"

        tk.Tk.__init__(self)
        self.OFFSET = 50
        self.WIDTH = 300
        self.HEIGHT = self.WIDTH

        self.title("Tic-Tac-Toe")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT + self.OFFSET}")
        self.resizable(False, False)

        self.score = [0, 0]
        self.score_variable = tk.StringVar()
        self.update_score()

        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg="white")
        self.canvas.place(x=0, y=self.OFFSET)

        self.label_score = tk.Label(self, textvariable=self.score_variable, justify=tk.CENTER, font=30)
        self.label_score.place(x=self.WIDTH / 2 - 20, y=20)

        self.update()

        if self.turn == "o":
            other_player_move = receive()
            col, row = int(other_player_move[0]), int(other_player_move[1])

            self.play(col, row, "x")
            self.waiting = False

        self.bind("<Button-1>", self.on_click)
        self.mainloop()

    def on_click(self, event):
        """
        Traduis les coordonnées du clic en ligne/colonne de la grille et joue
        à ces coordonnées si la case est libre.
        S'occupe aussi de la réception du coup adverse.
        """
        if event.widget != self.canvas and not self.waiting:
            return

        THIRD_WIDTH = self.WIDTH / 3
        THIRD_HEIGHT = self.HEIGHT / 3

        x, y = event.x, event.y

        row = int(y // (THIRD_HEIGHT))
        col = int(x // (THIRD_WIDTH))

        if not self.grid[row][col]:

            finished = self.play(col, row, self.turn)
            send(f"{col}{row}")
            if not finished:  # attendre une réponse seulement si la partie n'est pas finie

                self.waiting = True
                other_player_move = receive()  # attend la réponse de l'autre joueur
                col, row = int(other_player_move[0]), int(other_player_move[1])

                # joue pour l'autre joueur
                if self.turn == "x":
                    self.play(col, row, "o")
                else:
                    self.play(col, row, "x")
                self.waiting = False

    def play(self, col, row, turn):
        """
        Joue dans la grille aux coordonnées 'col' - 'row' en tant que joueur 'turn'
        et vérifie si la partie est finie (victoire / défaite / égalité).

        Renvoie True si la partie est finie.
        """
        self.grid[row][col] = turn
        color = "red" if turn == "x" else "green"
        self.create_circle(col, row, color)

        self.update()  # force la mise à jour de l'affichage

        if winner := self.check_winner():  # la partie est finie
            self.end_game(winner)
            return True

    def check_winner(self):
        """Fonction vérifiant si un des joueurs a gagné ou si le plateau est plein"""

        def nb_to_x_y_pair(n):
            """Converti l'index n de la représentation linéaire de la grille en un couple de coordonnées {x;y}"""
            y = n // 3
            x = n % 3
            return x, y

        for comb in TicTacToe.win_conditions:
            # vérifie toutes les possibilités pour le joueur 'x'
            if all(self.grid[xy[1]][xy[0]] == "x" for i in comb if (xy := nb_to_x_y_pair(i))):
                return "x"
            # vérifie toutes les possibilités pour le joueur 'o'
            elif all(self.grid[xy[1]][xy[0]] == "o" for i in comb if (xy := nb_to_x_y_pair(i))):
                return "o"
            # vérifie si la grille est vide
            elif all(self.grid[y][x] for x in range(3) for y in range(3)):
                return "tie"

    def end_game(self, winner):
        """S'occupe de la fin d'une partie (affichage des scores et réinitialisation)"""
        if winner == self.turn:
            self.score[0] += 1
            tkinter.messagebox.showinfo(title="Gagné !", message="Vous avez gagné !")
        elif winner == ("o" if self.turn == "x" else "x"):
            self.score[1] += 1
            tkinter.messagebox.showinfo(title="Perdu !", message="Le joueur adverse a gagné !")
        else:
            tkinter.messagebox.showinfo(title="Égalité !", message="Le plateau est plein et personne n'a gagné !")
        self.reset_game()

    def reset_game(self):
        """Remet à zéro toutes les variables afin de pouvoir recommencer une partie."""
        self.canvas.delete("all")
        self.grid = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.update_score()
        self.update()

        if self.turn == "o":
            self.waiting = True
            other_player_move = receive()
            col, row = int(other_player_move[0]), int(other_player_move[1])

            self.play(col, row, "x")
            self.waiting = False

    def update_score(self):
        """Met à jouer le label score"""
        self.score_variable.set(f"{self.score[0]} - {self.score[1]}")

    def create_circle(self, col, row, fill_color):
        """Créer un cercle de couleur 'fill_color' dans la grille aux coordonnées {col;row}"""
        THIRD_WIDTH = self.WIDTH / 3
        THIRD_HEIGHT = self.HEIGHT / 3

        offset = 10

        # coin haut gauche du cerlce de coordonné {x0; y0}
        x0 = col * THIRD_WIDTH + offset
        y0 = row * THIRD_HEIGHT + offset

        # coin bas droit du cerlce de coordonné {x1; y1}
        x1 = (col + 1) * THIRD_WIDTH - offset
        y1 = (row + 1) * THIRD_HEIGHT - offset

        self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color)


client_multi_socket = socket.socket()  # notre client

inp = input("Host IP adress (leave blank for localhost): ")

host = inp or "127.0.0.1"  # choisi localhost comme hôte si l'adresse IP rentrée en input est nulle
port = 2004

print("Waiting for connection response")
try:
    client_multi_socket.connect((host, port))
    print("Connection established with the server.")
except socket.error as e:
    print(e)


def send(msg):
    """Encode et envoie une chaine de caractère 'msg' au serveur"""
    client_multi_socket.send(str.encode(msg, "utf-8"))


def receive():
    """Reçoit une chaine de caractère du serveur, la décode et la renvoie."""
    return client_multi_socket.recv(1024).decode("utf-8")


player_number = receive()  # détermine si notre connection est la première ou la deuxième, ce qui détermine notre tour

game = TicTacToe(player_number)
client_multi_socket.close()
