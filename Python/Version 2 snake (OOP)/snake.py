from food import *
from neural_net import *
from main import *
import numpy as np

class Snake:

	global size

	def __init__(self, x, y):
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


	def move(self):
		self.lifetime += 1
		self.steps_to_live -= 1

		if self.steps_to_live < 0:
			self.alive = False

		if self.gonna_die(self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]):
			alive = False

		if self.pos[0] + self.vel[0] == self.food.pos[0] and self.pos[1] + self.vel[1] == self.food.pos[1]:
			self.eat()

