import tkinter as tk
import tkinter.messagebox

win_conditions = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


class TicTacToe(tk.Tk):
    def __init__(self):

        self.grid = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.turn = "x"

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

        self.bind("<Button-1>", self.on_click)
        self.mainloop()

    def on_click(self, event):
        if event.widget != self.canvas or self.turn == "stop":
            return

        x, y = event.x, event.y

        third_width = self.WIDTH / 3
        third_height = self.HEIGHT / 3

        col = int(x // (third_width))
        row = int(y // (third_height))

        if not self.grid[row][col]:
            self.grid[row][col] = self.turn
            color = "red" if self.turn == "x" else "green"
            self.create_circle(col, row, color)

            self.turn = "o" if self.turn == "x" else "x"

        self.update()

        if winner := self.check_winner():
            if winner == "x":
                self.score[0] += 1
                tkinter.messagebox.showinfo(title="Gagné !", message="Le joueur 1 a gagné !")
            elif winner == "o":
                self.score[1] += 1
                tkinter.messagebox.showinfo(title="Perdu !", message="Le joueur 2 a gagné !")
            else:
                tkinter.messagebox.showinfo(title="Égalité !", message="Le plateau est plein et personne n'a gagné !")
            self.turn = "stop"
            self.reset_game()

    def check_winner(self):
        def nb_to_x_y_pair(n):
            y = n // 3
            x = n % 3
            return x, y

        for comb in win_conditions:
            if all(self.grid[xy[1]][xy[0]] == "x" for i in comb if (xy := nb_to_x_y_pair(i))):
                return "x"
            elif all(self.grid[xy[1]][xy[0]] == "o" for i in comb if (xy := nb_to_x_y_pair(i))):
                return "o"
            elif all(self.grid[y][x] for x in range(3) for y in range(3)):
                return "tie"

    def reset_game(self):
        self.canvas.delete("all")
        self.grid = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.turn = "x"
        self.update_score()

    def update_score(self):
        self.score_variable.set(f"{self.score[0]} - {self.score[1]}")

    def create_circle(self, col, row, fill_color):
        third_width = self.WIDTH / 3
        third_height = self.HEIGHT / 3

        offset = 10

        x0 = col * third_width + offset
        y0 = row * third_height + offset

        x1 = (col + 1) * third_width - offset
        y1 = (row + 1) * third_height - offset

        self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color)


game = TicTacToe()
