"""
This sketch is written using the python mode of processing
There are several exemples below, uncomment one to see what gets drawn

!!! be sure to keep least and at most one turtle uncommented at a time !!!

press any key to draw the next step
"""

from Turtle2D import *
from random import random, choice
from math import floor
import re

WIDTH = 600
HEIGHT = 600

# parameters:
# axiom, rules, step, angle, drawn_variables=["F"], shrinking_coeff=0.85, line_color=255, transparency=0.3, stroke_weight=1, bg_color=51, x=WIDTH/2, y=HEIGHT

#turtle = Turtle2D("F", {"F": "F+[F-F]-F[+F]"}, 10, 25) # leaf like shape
#turtle = Turtle2D("F", {"F": "FF+[+F-F-F]-[-F+F+F]"}, 10, 25, transparency=0.5, line_color=0, bg_color=255)                                                                  # fractal tree
#turtle = Turtle2D("F", {"F": "F+F−F−F+F"}, 10, 90, transparency=1, shrinking_coeff=1, x=WIDTH/4, y=HEIGHT/1.3)                                                               # quad fractal
#turtle = Turtle2D("L", {"L": "+RF-LFL-FR+", "R": "-LF+RFR+FL-"}, 10, 90, transparency=1, x=0)                                                                                # Hilbert curve
#turtle = Turtle2D("FX", {"X": "X+YF+", "Y": "-FX-Y"}, 10, 90, shrinking_coeff=0.9, transparency=0.8, y=HEIGHT/2)                                                             # Dragon curve
#turtle = Turtle2D("FX", {"X": "YF+XF+Y", "Y": "XF-YF-X"}, 10, 60, shrinking_coeff=0.75, transparency=0.8)                                                                    # Arrowhead curve
#turtle = Turtle2D("FX", {"X": "X+YF++YF-FX--FXFX-YF+", "Y": "-FX+YFYF++YF+FX--FX-Y"}, 10, 60, shrinking_coeff=0.75, transparency=0.8, x=WIDTH/4, y=HEIGHT/3)                 # Peano-Gosper curve
#turtle = Turtle2D("FXF--FF--FF", {"X": "--FXF++FXF++FXF--", "F": "FF"}, 10, 60, shrinking_coeff=0.75, transparency=0.8, x=WIDTH/6*5)                                         # Sierpinski triangle
#turtle = Turtle2D("F-F-F-F-F", {"F": "F-F++F+F-F-F"}, 10, 72, shrinking_coeff=0.7, transparency=0.5, x=WIDTH/4, y=HEIGHT/2)                                                  # Snowflake
#turtle = Turtle2D("L--F--L--F", {"L": "+R-F-R+", "R": "-L+F+L-"}, 10, 45, shrinking_coeff=0.95, transparency=1)                                                              # Unknow shape
#turtle = Turtle2D("F--F--F", {"F": "F+F--F+F"}, 10, 60, shrinking_coeff=0.65, transparency=1, x=WIDTH/1.429, y=HEIGHT/6*5)                                                   # Koch fractal
#turtle = Turtle2D("X", {"F": "FF", "X": "F[+X][--X]FX"}, 10, 12, shrinking_coeff=0.8, transparency=1, stroke_weight=1.5)                                                     # tree
#turtle = Turtle2D("F+F+F+F", {"F": "FF+F++F+F"}, 10, 90, shrinking_coeff=0.76, transparency=1, stroke_weight=2, x=0)                                                         # Icy fractal
#turtle = Turtle2D("F", {"F": "F[+FF][-FF]F[-F][+F]F"}, 10, 36, shrinking_coeff=0.9, transparency=1, stroke_weight=1)                                                         # another tree
#turtle = Turtle2D("F", {"F": "F++F"}, 100, 77, shrinking_coeff=1.1, transparency=1, stroke_weight=1, x=WIDTH/3, y=HEIGHT/3*2)                                                # round star
#turtle = Turtle2D("F-F-F-F", {"F": "F-b+FF-F-FF-Fb-FF+b-FF+F+FF+Fb+FFF", "b": "bbbbbb"}, 10, 90, shrinking_coeff=0.6, transparency=1, stroke_weight=1, x=WIDTH/12*11)        # island curve
#turtle = Turtle2D("A", {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"}, 10, 60, ["A", "B"], shrinking_coeff=0.85, transparency=1, stroke_weight=1, x=WIDTH/6*5, y=HEIGHT/3) # Gosper curve
#turtle = Turtle2D("[7]++[7]++[7]++[7]++[7]", {"6": "81++91----71[-81----61]++", "7": "+81--91[---61--71]+", "8": "-61++71[+++81++91]-", \
#            "9": "--81++++61[+91++++71]--71", "1": ""}, 10, 36, ["6", "7", "8", "9"], shrinking_coeff=1, transparency=1, stroke_weight=1, x=WIDTH/2, y=HEIGHT/2)             # Penrose tiling

def generate_turtle():
	''' 
	generate a Turtle2D object with random axiom, rules, drawn variables, angle etc...
	'''

	def get_random_number_with_fallof(start=0, end=10, exponent=2):
		return int(floor(pow(random(), exponent) * (end-start)) + start)

	def generate_letters():
		nb_letters = get_random_number_with_fallof(1, 10, 2)

		letters = ''
		while len(letters) != nb_letters:
			new_letter = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
			if new_letter not in letters:
				letters += new_letter

		return letters

	def generate_axiom(letters):
		symbols1 = "+-["
		symbols2 = "+-]"
	
		axiom_length = get_random_number_with_fallof(1, 20, 2)
	
		axiom = ''
		while not(re.search('[A-Z]', axiom)) or axiom.count('[') != axiom.count(']'):
			for _ in range(axiom_length):
				possibilities = symbols1 + letters if axiom.count('[') <= axiom.count(']') else symbols2 + letters
				axiom += choice(possibilities)
	
		return axiom
	
	def generate_rule(letters):
		symbols1 = "+-["
		symbols2 = "+-]"
	
		rule_length = get_random_number_with_fallof(1, 10, 2)
	
		rule = ''
		while not(re.search('[A-Z]', rule)) or rule.count('[') != rule.count(']'):
			for _ in range(rule_length):
				possibilities = symbols1 + letters if rule.count('[') <= rule.count(']') else symbols2 + letters
				rule += choice(possibilities)
	
		return rule

	def generate_rules(letters):
		rules = {}
		for letter in letters:
			while not re.search('[A-Z]', rules.get(letter, '1')):
				rules[letter] = generate_rule(letters)

		return rules

	def pick_drawn_variables(letters, proba=0.8):
		pick = []
		while not pick:
			pick = [letter for letter in letters if random() <= proba]
		return pick

	def choose_angle(): 
	    return random() * 15 + 5
        # return choice([i*5 for i in range(1, 19)])

	STEP = 10

	letters = generate_letters()
	axiom = generate_axiom(letters)
	rules = generate_rules(letters)
	angle = choose_angle()
	drawn_variables = pick_drawn_variables(letters)

	return Turtle2D(axiom, rules, STEP, angle, drawn_variables, shrinking_coeff=1, line_color=255, transparency=1, stroke_weight=1, bg_color=51, x=WIDTH/2, y=HEIGHT/2)

def setup():
	global turtle
	size(WIDTH, HEIGHT, P2D)

	turtle = generate_turtle()

	turtle.draw_shape()
	
def draw(): # draw need to be here in order for 'keyPressed' to work
	pass
	
def keyPressed():
    global turtle
    if key == 'p':
        print(repr(turtle))
    elif key=='g':
        turtle = generate_turtle()
        turtle.draw_shape()
    else:
        turtle.generate_next()
        turtle.draw_shape()
	
