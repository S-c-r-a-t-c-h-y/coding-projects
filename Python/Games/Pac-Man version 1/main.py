from tkinter import *
import tkinter.messagebox
import time
import os
from typing import List, Optional, Callable
from random import choice
from Astar import *


WIDTH, HEIGHT = 380, 440
SCALE = 20
Pos = List[int]

class Pacman:
    # class that stocks every variables of pacman
    def __init__(self, pos: Pos):

        self.pos: Pos = pos
        self.lives: int = 3
        self.score: int = 0
        self.invincible: bool = False
        self.direction: str = 'up'
        self.last_direction: str = 'up'
        self.step: int = 1
        self.eat_counter: int = 0


    def move(self, direction: str, cnt: int = 0) -> None:

        if cnt > 975:
            return
        
        # up
        if direction == 'up':
            if self.pos[0] % SCALE == 0:
                if [self.pos[0], self.pos[1] - SCALE] not in walls:
                    self.pos[1] -= self.step
                else:
                    self.direction = ''
            else:
                self.move(self.last_direction, cnt + 1)

        # down
        elif direction == 'down':
            if self.pos[0] % SCALE == 0:
                if [self.pos[0], self.pos[1] + SCALE] not in walls and [self.pos[0], self.pos[1] + SCALE] != [9 * SCALE, 9 * SCALE]:
                    self.pos[1] += self.step
                else:
                    self.direction = ''
            else:
                self.move(self.last_direction, cnt + 1)

        # left
        elif direction == 'left':
            if self.pos[1] % SCALE == 0:
                if [self.pos[0] - SCALE, self.pos[1]] not in walls:
                    self.pos[0] -= self.step
                else:
                    self.direction = ''
            else:
                self.move(self.last_direction, cnt + 1)

        # right
        elif direction == 'right':
            if self.pos[1] % SCALE == 0:
                if [self.pos[0] + SCALE, self.pos[1]] not in walls:
                    self.pos[0] += self.step
                else:
                    self.direction = ''
            else:
                self.move(self.last_direction, cnt + 1)

        if self.pos[0] < -SCALE:
            self.pos[0] = WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] = -SCALE


    def up(self, event) -> None:

        self.last_direction = self.direction if self.direction != '' else 'up'
        self.direction = 'up'

    def down(self, event) -> None:
        self.last_direction = self.direction if self.direction != '' else 'down'
        self.direction = 'down'

    def left(self, event) -> None:
        self.last_direction = self.direction if self.direction != '' else 'left'
        self.direction = 'left'

    def right(self, event) -> None:
        self.last_direction = self.direction if self.direction != '' else 'right'
        self.direction = 'right'


    def set_invincible(self) -> None:
        ''' 
        if pacman is not invincible, it sets him invincible and vice versa
        '''

        self.invincible = not self.invincible
        self.eat_counter = 0
        for ghost in ghosts:
            ghost.frightened = not ghost.frightened


    def get_index(self) -> tuple: return self.pos[0] // SCALE, self.pos[1] // SCALE


    def draw(self) -> None:
        '''
        draws pacman using the sprites
        '''
        if framecount % 2:
            if self.direction == 'right': canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=right, tags='pacman')
            if self.direction == 'left': canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=left, tags='pacman')
            if self.direction == 'up': canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=up, tags='pacman')
            if self.direction == 'down': canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=down, tags='pacman')
            if self.direction == '':  canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=idle, tags='pacman')
        else:
            canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=idle, tags='pacman')

class Ghost:

    def __init__(self, pos: Pos, name: str):
        self.pos: Pos = pos
        self.name: str = name
        self.alive: bool = True
        self.frightened: bool = False
        self.step: float = 1
        self.direction: str = 'up'
        self.last_direction: str = 'up'
        self.target: Optional[tuple] = None
        self.state: str = 'chase'


    def move(self, direction: str) -> None:

        self.step = .5 if self.frightened else 1
        
        if not self.frightened and self.pos[0] % 1 != 0:
            self.pos[0] += .5

        if not self.frightened and self.pos[1] % 1 != 0:
            self.pos[1] += .5

        # up
        if direction == 'up':
            if (
                self.pos[0] % SCALE == 0
                and [self.pos[0], self.pos[1] - SCALE] not in walls
            ):
                self.pos[1] -= self.step


        elif direction == 'down':
            if (
                self.pos[0] % SCALE == 0
                and [self.pos[0], self.pos[1] + SCALE] not in walls
            ):
                self.pos[1] += self.step

        elif direction == 'left':
            if (
                self.pos[1] % SCALE == 0
                and [self.pos[0] - SCALE, self.pos[1]] not in walls
            ):
                self.pos[0] -= self.step

        elif direction == 'right':
            if (
                self.pos[1] % SCALE == 0
                and [self.pos[0] + SCALE, self.pos[1]] not in walls
            ):
                self.pos[0] += self.step

        if self.pos[0] < -SCALE:
            self.pos[0] = WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] = -SCALE


    def select_direction(self) -> None:

        global walls_indices

        if not self.frightened or not self.alive:
            self.find_target()
            
            if 7 * SCALE <= self.pos[0] <= 11 * SCALE and (self.pos[1] == 16 * SCALE or self.pos[1] == 20 * SCALE):
                walls_indices.append([8, 15])
                walls_indices.append([10, 15])
                walls_indices.append([8, 19])
                walls_indices.append([10, 19])

            if self.direction == 'up':
                walls_indices.append([self.pos[0] // SCALE, self.pos[1] // SCALE + 1])
            elif self.direction == 'down':
                walls_indices.append([self.pos[0] // SCALE, self.pos[1] // SCALE - 1])
            elif self.direction == 'left':
                walls_indices.append([self.pos[0] // SCALE + 1, self.pos[1] // SCALE])
            elif self.direction == 'right':
                walls_indices.append([self.pos[0] // SCALE - 1, self.pos[1] // SCALE])

            solver = AStar(walls_indices, (self.pos[0] // SCALE, self.pos[1] // SCALE), self.target)
            next_step = solver.process()
            
            while len(walls_indices) != 238:
                walls_indices.pop()

            if next_step is not None:
                if next_step[0] < self.pos[0] // SCALE:
                    self.direction = 'left'
                elif next_step[0] > self.pos[0] // SCALE:
                    self.direction = 'right'
                elif next_step[1] < self.pos[1] // SCALE:
                    self.direction = 'up'
                elif next_step[1] > self.pos[1] // SCALE:
                    self.direction = 'down'
            else:
                self.select_random_direction()

        else:
            self.select_random_direction()


    def find_target(self) -> None:
        ''' 
        find the target tile of the ghost depending on its name and state
        according to the original pacman ghost AI
        '''

        if not self.alive:
            self.target = 9, 10
            return

        if self.frightened:
            return

        if self.state == 'chase':
            pac_x, pac_y = pacman.get_index()

            # pinky's target tile is 4 tile in front of pacman
            # except when up (because of the original pacman code)
            if self.name == 'pinky':
                direction = pacman.direction if pacman.direction != '' else pacman.last_direction
                if direction == 'up':
                    self.target = pac_x - 4, pac_y - 4 
                elif direction == 'down':
                    self.target = pac_x, pac_y + 4
                elif direction == 'left':
                    self.target = pac_x - 4, pac_y
                elif direction == 'right':
                    self.target = pac_x + 4, pac_y

            # blinky's target tile is pacman's position
            elif self.name == 'blinky':
                self.target = pac_x, pac_y

            # inky's target tile is depending on pacman's position
            # and blinky's position (too much detail to explain)
            elif self.name == 'inky':
                direction = pacman.direction if pacman.direction != '' else pacman.last_direction
                intermediate = ()
                if direction == 'up':
                    intermediate = pac_x, pac_y - 2 
                elif direction == 'down':
                    intermediate = pac_x, pac_x + 2
                elif direction == 'left':
                    intermediate = pac_x - 2, pac_y
                elif direction == 'right':
                    intermediate = pac_x + 2, pac_y

                blinky: 'Ghost' = ghosts[0]
                vect: List[int] = [- (blinky.pos[0] // SCALE - intermediate[0]), - (blinky.pos[1] // SCALE - intermediate[1])]

                self.target = intermediate[0] + vect[0], intermediate[1] + vect[1]

            # clyde's target tile is the same as blinky's one if he is more
            # than 5 tiles away form pacman
            elif self.name == 'clyde':
                if distance(self.pos[0], self.pos[1], pacman.pos[0], pacman.pos[1]) / SCALE >= 5:
                    self.target = pac_x, pac_y
                else:
                    self.target = 1, 20

        else: # scatter mode
            if self.name == 'blinky': self.target = 17, 1
            elif self.name == 'pinky': self.target = 1, 1
            elif self.name == 'inky': self.target = 17, 20
            elif self.name == 'clyde': self.target = 1, 20

        self.target = 0, self.target[1] if self.target[0] < 0 else 18, self.target[1] if self.target[0] >= 19 else self.target
        self.target = self.target[0], 0 if self.target[1] < 0 else self.target[0], 21 if self.target[1] >= 22 else self.target

    def select_random_direction(self) -> None:
        possible: list = ['up', 'right', 'left', 'down']
        dir_index: int = possible.index(self.direction)
        possible.reverse()
        inverse_dir: str = possible[dir_index]

        self.last_direction = self.direction
        self.direction = inverse_dir

        while self.direction == inverse_dir:
            self.direction = choice(possible)

    def print_target(self) -> None:
        self.find_target()
        canvas.create_rectangle(self.target[0] * SCALE, self.target[1] * SCALE, self.target[0] * SCALE + SCALE, \
         self.target[1] * SCALE + SCALE, outline='red', fill='red')
      
    def is_on_junction(self) -> bool:
        
        if self.pos[0] % SCALE == 0 and self.pos[1] % SCALE == 0:
            if self.direction in ['up', 'down']:
                if [self.pos[0] + SCALE, self.pos[1]] not in walls or \
                   [self.pos[0] - SCALE, self.pos[1]] not in walls:
                    return True
            elif self.direction in ['left', 'right']:
                if [self.pos[0], self.pos[1] + SCALE] not in walls or \
                   [self.pos[0], self.pos[1] - SCALE] not in walls:
                    return True

            # prevent ghosts from being stuck in the begining area
            if (
                    ([self.pos[0] + SCALE, self.pos[1]] not in walls) ^
                    ([self.pos[0] - SCALE, self.pos[1]] not in walls) ^
                    ([self.pos[0], self.pos[1] + SCALE] not in walls) ^
                    ([self.pos[0], self.pos[1] - SCALE] not in walls)
                ):
                return True

        return False

    def draw(self) -> None:

        if not self.alive:
            canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=eyes_img, tags='ghost')
        elif self.frightened:
            canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=vulnerable, tags='ghost')
        else:
            if self.name == 'inky':
                canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=inky_img, tags='ghost')
            if self.name == 'pinky':
                canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=pinky_img, tags='ghost')
            if self.name == 'blinky':
                canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=blinky_img, tags='ghost')
            if self.name == 'clyde':
                canvas.create_image(self.pos[0] + SCALE / 2, self.pos[1] + SCALE / 2, image=clyde_img, tags='ghost')

# ------------------------------------------------------------------------------------------------------------------

def update() -> None:
    '''
    function called each frame after 'delay' microseconds
    '''

    global framecount, difficulty, invincible_time

    draw()

    try:
        #ghosts[0].print_target()
        pass 
    except:
        pass

    # grid is empty
    if not balls and not powers:
        setup()
        difficulty += 1
        invincible_time = 9 - difficulty
        time.sleep(1)

    # repeat the process 4 times for it to be smooth
    for _ in range(difficulty):

        # when eating balls
        if pacman.pos in balls:
            balls.remove(pacman.pos)
            pacman.score += 10    
            score_label.set(f'{pacman.score}')

        # when eating power ups
        if pacman.pos in powers:
            powers.remove(pacman.pos)
            pacman.score += 50
            score_label.set(f'{pacman.score}')

            pacman.set_invincible()
            canvas.after(invincible_time * 1000, pacman.set_invincible)


        for ghost in ghosts:

            if ghost.pos == [9 * SCALE, 10 * SCALE]:
                ghost.alive = True
                ghost.direction = 'up'

            # checking for collision with ghosts
            if distance(pacman.pos[0], pacman.pos[1], ghost.pos[0], ghost.pos[1]) <= SCALE / 10: # touchs

                # pacman gets eaten
                if not pacman.invincible and ghost.alive:
                    pacman.lives -= 1
                    if pacman.lives == 0:
                        retry()

                    time.sleep(1)
                    setup()

                # pacman eats the ghost
                elif pacman.invincible and ghost.alive:
                    ghost.alive = False
                    pacman.score += 200 * 2 ** pacman.eat_counter
                    pacman.eat_counter += 1
                    score_label.set(f'{pacman.score}')

        canvas.delete('pacman')
        pacman.draw()

        canvas.delete('ghost')
        for ghost in ghosts:
            ghost.draw()

        
        pacman.move(pacman.direction)
        for ghost in ghosts:
            if ghost.is_on_junction():
                ghost.select_direction()
            ghost.move(ghost.direction)

    framecount += 1
    top.after(delay, update)

# ------------------------------------------------------------------------------------------------------------------

def draw() -> None:
    '''
    draws the walls, balls and power-ups on the canvas
    '''

    canvas.delete('all')

    # draws each walls
    for wall in walls:
        canvas.create_rectangle(wall[0], wall[1], wall[0] + SCALE, wall[1] + SCALE, outline='blue4', fill='blue4')

    # draws each balls
    for ball in balls:
        canvas.create_oval(ball[0] + SCALE / 2.5, ball[1] + SCALE / 2.5, ball[0] + SCALE / 1.5, ball[1] + SCALE / 1.5, outline='white', fill='yellow')

    # draws each balls
    for power in powers:
        canvas.create_oval(power[0] + SCALE / 4, power[1] + SCALE / 4, power[0] + SCALE / 1.2, power[1] + SCALE / 1.2, outline='white', fill='white')

# ------------------------------------------------------------------------------------------------------------------

def distance(xa, ya, xb, yb) -> float: return ((xb-xa)**2 + (yb-ya)**2) ** 0.5

# ------------------------------------------------------------------------------------------------------------------

def wait(remaining_time: float, callback: Callable, *args) -> None:
    remaining_time -= 0.1
    if remaining_time > 0:
        top.after(100, wait, remaining_time, callback, *args)
    else:
        callback(*args)

# ------------------------------------------------------------------------------------------------------------------

def retry() -> None:
 
    tkinter.messagebox.showinfo(title='Perdu !', message=f"Vous n'avez plus de vie !")
    top.destroy()

# ------------------------------------------------------------------------------------------------------------------

def create_walls() -> None:

    global walls, walls_indices
    walls = []

    # up / down
    for i in range(int(WIDTH // SCALE / 2 - .5)):
        walls.append([i * SCALE, 0])
        walls.append([i * SCALE, HEIGHT - SCALE])

    # left / right
    for i in range(HEIGHT // SCALE):
        walls.append([0, i * SCALE])

    # extremen left / right
    for j in range(7, 14, 2):
        for i in range(4):
            walls.append([i * SCALE, j * SCALE])

    # big left / right horizontal bar
    
    for i in range(6):
        walls.append([(i + 2) * SCALE, 19 * SCALE])


    for i in range(3):
        walls.append([(i + 5) * SCALE, 15 * SCALE])

    for i in range(3):
        walls.append([5 * SCALE, (i + 11) * SCALE])

    for i in range(5):
        walls.append([5 * SCALE, (i + 5) * SCALE])

    for i in range(2):
        walls.append([(i + 7) * SCALE, 5 * SCALE])

    for i in range(2):
        walls.append([(i + 7) * SCALE, 9 * SCALE])

    for i in range(2):
        walls.append([(i + 7) * SCALE, 11 * SCALE])

    for i in range(2):
        walls.append([(i + 7) * SCALE, 13 * SCALE])

    for i in range(2):
        walls.append([(i + 7) * SCALE, 17 * SCALE])

    for i in range(3):
        walls.append([3 * SCALE, (i + 15) * SCALE])

    for i in range(2):
        walls.append([(i + 2) * SCALE, 2 * SCALE])
    for i in range(2):
        walls.append([(i + 2) * SCALE, 3 * SCALE])
    for i in range(2):
        walls.append([(i + 2) * SCALE, 5 * SCALE])

    for i in range(3):
        walls.append([(i + 5) * SCALE, 2 * SCALE])
    for i in range(3):
        walls.append([(i + 5) * SCALE, 3 * SCALE])

    # middle
    for i in range(4):
        walls.append([9 * SCALE, i * SCALE])
    for i in range(3):
        walls.append([9 * SCALE, (i + 17) * SCALE])
    for i in range(3):
        walls.append([9 * SCALE, (i + 13) * SCALE])
    for i in range(3):
        walls.append([9 * SCALE, (i + 5) * SCALE])

    wanted_walls = [[3 * SCALE, 8 * SCALE], [3 * SCALE, 12 * SCALE], [1 * SCALE, 17 * SCALE], \
                    [5 * SCALE, 18 * SCALE], [5 * SCALE, 17 * SCALE], [9 * SCALE, HEIGHT - SCALE], \
                    [2 * SCALE, 15 * SCALE], [9 * SCALE, 11 * SCALE], [7 * SCALE, 10 * SCALE], \
                    [6 * SCALE, 7 * SCALE], [7 * SCALE, 7 * SCALE]]

    for wall in wanted_walls:
        walls.append(wall)

    unwanted_walls = [[0, 8 * SCALE], [0, 10 * SCALE], [0, 12 * SCALE]]

    walls = [e for e in walls if e not in unwanted_walls]

    walls2 = []
    for wall in walls:
        walls2.append([WIDTH - wall[0] - SCALE, wall[1]])
    walls.extend(walls2)
    
    walls_indices = []
    for wall in walls:
        walls_indices.append([wall[0] // SCALE, wall[1] // SCALE])

# ------------------------------------------------------------------------------------------------------------------

def create_ghost(name: str) -> None:
    ghosts.append(Ghost([9 * SCALE, 10 * SCALE], name))

# ------------------------------------------------------------------------------------------------------------------

def setup() -> None:

    global balls, powers, ghosts

    pacman.pos = [180, 320]
    balls = []
    powers = []

    # creates every balls
    for i in range(WIDTH // SCALE):
        for j in range(HEIGHT // SCALE):
            if [i * SCALE, j * SCALE] not in walls and [i * SCALE, j * SCALE] != pacman.pos:
                balls.append([i * SCALE, j * SCALE])

    # remove all the balls that are in unwanted places
    for i in range(len(balls)-1, -1, -1):
        if 5 * SCALE <= balls[i][0] <= 13 * SCALE and 7 * SCALE <= balls[i][1] <= 13 * SCALE:
            balls.pop(i)
        if 0 * SCALE <= balls[i][0] <= 3 * SCALE and 7 * SCALE <= balls[i][1] <= 13 * SCALE:
            balls.pop(i)
        if 15 * SCALE <= balls[i][0] <= 19 * SCALE and 7 * SCALE <= balls[i][1] <= 13 * SCALE:
            balls.pop(i)

    # replace certain balls by power-ups
    balls.remove([SCALE, 3 * SCALE])
    powers.append([SCALE, 3 * SCALE])

    balls.remove([SCALE, 16 * SCALE])
    powers.append([SCALE, 16 * SCALE])

    balls.remove([(WIDTH // SCALE - 2) * SCALE, 3 * SCALE])
    powers.append([(WIDTH // SCALE - 2) * SCALE, 3 * SCALE])

    balls.remove([(WIDTH // SCALE - 2) * SCALE, 16 * SCALE])
    powers.append([(WIDTH // SCALE - 2) * SCALE, 16 * SCALE])

    # create ghosts
    ghosts = []

    wait(0, create_ghost, 'blinky')
    
    wait(2, create_ghost, "pinky")
    wait(5, create_ghost, "inky")
    wait(7, create_ghost, "clyde")
    
    

# ------------------------------------------------------------------------------------------------------------------

def main() -> None:

    global canvas, pacman, score_label, balls, powers, framecount, delay, invincible_time, difficulty
    global idle, right, left, up, down
    global inky_img, pinky_img, blinky_img, clyde_img, vulnerable, eyes_img

    canvas = Canvas(top, width=WIDTH, height=HEIGHT, bg='grey10', bd=0)
    canvas.place(x=0, y=30)

    pacman = Pacman([300, 300])

    framecount = 0
    delay = 50
    difficulty = 4
    invincible_time = 5

    current_dir = os.getcwd()
    # creating every photo image
    idle = PhotoImage(file=f"{current_dir}\\sprites\\idle.png")
    up = PhotoImage(file=f"{current_dir}\\sprites\\up.png")
    right = PhotoImage(file=f"{current_dir}\\sprites\\right.png")
    down = PhotoImage(file=f"{current_dir}\\sprites\\down.png")
    left = PhotoImage(file=f"{current_dir}\\sprites\\left.png")

    inky_img = PhotoImage(file=f"{current_dir}\\sprites\\inky.png")
    pinky_img = PhotoImage(file=f"{current_dir}\\sprites\\pinky.png")
    blinky_img = PhotoImage(file=f"{current_dir}\\sprites\\blinky.png")
    clyde_img = PhotoImage(file=f"{current_dir}\\sprites\\clyde.png")
    vulnerable = PhotoImage(file=f"{current_dir}\\sprites\\vulnerable.png")
    eyes_img = PhotoImage(file=f"{current_dir}\\sprites\\eyes.png")
    
    create_walls()
    setup()

    score_label = StringVar()
    score_label.set(f'{pacman.score}')
    label_score = Label(top, textvariable=score_label, font='Times 15 bold', bg='black', fg='white', height=1, width=12)
    label_score.place(x=100, y=0)
    
    update()

    top.bind("<z>", pacman.up)
    top.bind("<s>", pacman.down)
    top.bind("<q>", pacman.left)
    top.bind("<d>", pacman.right)
    top.mainloop()

if __name__ == '__main__':
    top = Tk()
    top.title("PacMan")
    top.geometry(f'{WIDTH+5}x{HEIGHT+60}') #30x22
    top.configure(bg='black')
    top.resizable(width=False, height=False)
    
    main()
