from random import choice

c = 0
inc = 10
square = [PVector(0, 1), PVector(0, -1), PVector(1, 0), PVector(-1, 0)]
diagonal = [PVector(1, 1), PVector(-1, -1), PVector(1, -1), PVector(-1, 1)]
losange = [PVector(1, .5), PVector(-1, -.5), PVector(1, -.5), PVector(-1, .5)]


def setup():
	global x, y

	colorMode(HSB, 360, 100, 100)
	size(400, 400)
	background(51)

	x, y = width/2, height/2


def draw():
	global c, x, y
	stroke(c, 100, 100)

	v = choice(square) * inc
	# v = choice(diagonal) * inc
	# v = choice(losange) * inc

	line(x, y, x + v.x, y + v.y)
	x, y = x + v.x, y + v.y

	if x < inc:
		x = width - inc
	elif x > width - inc:
		x = inc

	if y < inc:
		y = height - inc
	elif y > height - inc:
		y = inc


	c += 1
	if c > 360:
		c -= 360
