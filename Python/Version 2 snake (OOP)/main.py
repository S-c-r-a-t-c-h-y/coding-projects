import numpy as np
from math import floor
import csv

class Snake:

    global size

    def __init__(self):
        x = 600
        y = 200
        self.pos = np.array([x, y])
        self.tail = [np.array([x-3*size, y]), np.array([x-2*size, y]), np.array([x-size, y])]
        self.len = 4
        self.steps_to_live = 200
        self.fitness = 0
        self.lifetime = 0
        self.vel = np.array([size, 0])
        self.food = Food()
        self.brain = Neural_Net(24, 18, 4)
        self.alive = True
        self.grow_count = 0
        self.testing = False
        self.decision = []
        self.vision = []

    # -----------------------------------------------------------------------------------------------------------------------

    def set_velocity():
        self.decision = self.brain.output(self.vision)

        max = 0
        max_index = 0
        for i in range(len(self.decision)):
            if max > self.decision[i]:
                max = self.decision[i]:
                max_index = i

        if max_index == 0:
            self.vel[0] = -10
            self.vel[1] = 0
        elif max_index == 1:
            self.vel[0] = 0
            self.vel[1] = -10
        elif max_index == 2:
            self.vel[0] = 10
            self.vel[1] = 0
        elif max_index == 3:
            self.vel[0] = 0
            self.vel[1] = 10


    # -----------------------------------------------------------------------------------------------------------------------

    def move(self):
        self.lifetime += 1
        self.steps_to_live -= 1

        if self.steps_to_live < 0:
            self.alive = False

        if self.gonna_die(self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]):
            alive = False

        if self.pos[0] + self.vel[0] == self.food.pos[0] and self.pos[1] + self.vel[1] == self.food.pos[1]:
            self.eat()

        if self.grow_count > 0:
            self.grow_count -= 1
            self.grow()
        else:
            for i in range(len(self.tail)):
                self.tail[i] = np.array([self.tail[i+1][0], self.tail[i+1][1]])
            self.tail[self.len - 2] = np.array([self.pos[0], self.pos[1]])

        self.pos += vel

    # -----------------------------------------------------------------------------------------------------------------------

    def eat():

        self.food = Food()
        while self.food.pos in self.tail:
            self.food = Food()

        self.steps_to_live += 100

        if self.testing or len >= 10:
            self.grow_count += 4
        else:
            self.grow_count += 1

    # -----------------------------------------------------------------------------------------------------------------------

    def grow():
        self.tail.append(np.array([self.pos[0], self.pos[1]]))
        self.len += 1

    # -----------------------------------------------------------------------------------------------------------------------

    def gonna_die(x: float, y: float) -> bool:
        if x < 400 or y < 0 or x >= 800 or y >= 400: return True
        return self.is_on_tail(x, y)

    # -----------------------------------------------------------------------------------------------------------------------

    def is_on_tail(x: float, y: float) -> bool:
        return True if np.array([x, y]) in self.tail else False

    # -----------------------------------------------------------------------------------------------------------------------

    def calc_fitness():
        if self.len < 10:
            self.fitness = floor(self.lifetime * self.lifetime * 2 ** floor(self.len))
        else:
            self.fitness = lifetime ** 2
            self.fitness *= 2 ** 10
            self.fitness *= (self.len - 9)

    # -----------------------------------------------------------------------------------------------------------------------

    def crossover(partner: Snake) -> Snake:
        child = Snake()

        child.brain = brain.crossover(partner.brain)
        return child

    # -----------------------------------------------------------------------------------------------------------------------

    def clone() -> Snake:
        clone = Snake()
        clone.brain = brain.clone()
        clone.alive = True
        return clone

    # -----------------------------------------------------------------------------------------------------------------------

    def save_snake(snake_no, score, pop_ID):

        heading = ['Top Score', 'PopulationID']
        data = [{'Top Score': score, 'PopulationID': pop_ID}]

        write(f'data/SnakesStats{snake_no}.csv', data, heading)

        # ATTENTION CECI N'EST PAS FINI !!!!!
        # ATTENTION CECI N'EST PAS FINI !!!!!
        # ATTENTION CECI N'EST PAS FINI !!!!!
        # ATTENTION CECI N'EST PAS FINI !!!!!
        # ATTENTION CECI N'EST PAS FINI !!!!!

    # -----------------------------------------------------------------------------------------------------------------------

    def load_snake(snake_no):
        load = Snake()

        data, heading = [], []

        read(f'data/SnakesStats{snake_no}.csv', data, heading)

        # ATTENTION CECI N'EST PAS FINI !!!!!
        # ATTENTION CECI N'EST PAS FINI !!!!!
        # ATTENTION CECI N'EST PAS FINI !!!!!
        # ATTENTION CECI N'EST PAS FINI !!!!!
        # ATTENTION CECI N'EST PAS FINI !!!!!

    # -----------------------------------------------------------------------------------------------------------------------

    def look():
        self.vision = [_ for _ in range(24)]

        #left
        temp_values = self.look_in_direction(np.array([-10, 0]))
        self.vision[0] = temp_values[0]
        self.vision[1] = temp_values[1]
        self.vision[2] = temp_values[2]
        #left-up
        temp_values = self.look_in_direction(np.array([-10, -10]))
        self.vision[3] = temp_values[1]
        self.vision[4] = temp_values[2]
        self.vision[5] = temp_values[3]
        #up
        temp_values = self.look_in_direction(np.array([0, -10]))
        self.vision[6] = temp_values[1]
        self.vision[7] = temp_values[2]
        self.vision[8] = temp_values[3]
        #up-right
        temp_values = self.look_in_direction(np.array([10, -10]))
        self.vision[9] = temp_values[1]
        self.vision[10] = temp_values[2]
        self.vision[11] = temp_values[3]
        #right
        temp_values = self.look_in_direction(np.array([10, 0]))
        self.vision[12] = temp_values[1]
        self.vision[13] = temp_values[2]
        self.vision[14] = temp_values[3]
        #right-down
        temp_values = self.look_in_direction(np.array([10, 10]))
        self.vision[15] = temp_values[1]
        self.vision[16] = temp_values[2]
        self.vision[17] = temp_values[3]
        #down
        temp_values = self.look_in_direction(np.array([0, 10]))
        self.vision[18] = temp_values[1]
        self.vision[19] = temp_values[2]
        self.vision[20] = temp_values[3]
        #down-left
        temp_values = self.look_in_direction(np.array([-10, 10]))
        self.vision[21] = temp_values[1]
        self.vision[22] = temp_values[2]
        self.vision[23] = temp_values[3]

    # -----------------------------------------------------------------------------------------------------------------------

    def look_in_direction(direction):
        vision_in_direction = [_ for _ in range(3)]

        position = np.array([self.pos[0] , self.pos[1]])
        food_is_found = False
        tail_is_found = False
        distance = 0

        position += direction
        distance += 1

        while not(position[0] < 400 or position[1] < 0 or position[0] >= 800 or position[1] >= 400):

            if not(food_is_found and position[0] == self.food.pos[0] and position[1] == self.food.pos[1]):
                vision_in_direction[0] = 1
                food_is_found = True

            if not(tail_is_found and self.is_on_tail(position[0], position[1])):
                vision_in_direction[1] = 1/distance
                tail_is_found = True

            position += direction
            distance += 1

        vision_in_direction[2] = 1/distance

        return vision_in_direction


# -----------------------------------------------------------------------------------------------------------------------------




def read(file, data, heading):

    with open(file, "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        heading.extend(reader.fieldnames)
        for row in reader:
            data.append(dict(row))


def write(file, data, heading):

    with open(file, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=heading, delimiter=';')
        writer.writeheader()
        writer.writerows(data)


def main():
    
    # initialisation de la fenêtre
    global fenetre
    fenetre = Tk()
    fenetre.title("Jeu du snake")
    fenetre.geometry('600x600')
    fenetre.configure(bg='white')
    fenetre.resizable(width=False, height=False)

    global size
    size = 10

    # canvas sur lequel le serpent et la pomme sont dessinés
    global canvas, snake, direction, derniere_direction
    canvas = Canvas(fenetre, width=600, height=495, bg='gray25')
    canvas.pack()

    # initialisation du serpent : c'est une liste de liste contenant les coordonnées de son corps
    # l'élément d'index -1 contient sa tête et l'élément d'index 0 sa queue
    x0 = 300
    y0 = 300
    snake = [[x0 + 3 * taille_carre, y0], [x0 + 2 * taille_carre, y0], [x0 + taille_carre, y0], [x0, y0]]
    direction = 'left'
    derniere_direction = direction

    # création des boutons 'recommencer', 'commencer' et 'quitter'
    bouton_recommencer = Button(fenetre, text='recommencer', command=recommencer, width=26, height=6, bg='grey')
    bouton_recommencer.pack(side=LEFT)

    bouton_commencer = Button(fenetre, text='commencer', command=commencer, width=26, height=6, bg='grey', padx=15)
    bouton_commencer.pack(side=LEFT)

    bouton_quitter = Button(fenetre, text='quitter', command=fenetre.destroy, width=26, height=6, bg='grey')
    bouton_quitter.pack(side=RIGHT)

    # linkage des touches 'zqsd' du clavier avec les fonctions qui permettent de changer la direction du serpent
    fenetre.bind("<z>", up)
    fenetre.bind("<s>", down)
    fenetre.bind("<q>", left)
    fenetre.bind("<d>", right)
    fenetre.mainloop()

if __name__ == '__main__':
    main()