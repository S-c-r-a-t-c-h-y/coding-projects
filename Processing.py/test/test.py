from random import random, choice
from math import floor
import re



def generate_turtle():

	STEP = 10

	letters = generate_letters()
	axiom = generate_axiom(letters)
	rules = generate_rules(letters)
	angle = choose_angle()
	drawn_variables = pick_drawn_variables(letters)

	return Turtle2D(axiom, rules, STEP, angle, drawn_variables, shrinking_coeff=0.85, line_color=255, transparency=1, stroke_weight=1, bg_color=51, x=None, y=None)

''' 
generate a Turtle2D object with random axiom, rules, drawn variables, angle etc...
'''

def get_random_number_with_fallof(start=0, end=10, exponent=2):
	return floor(pow(random(), exponent) * (end-start)) + start

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

def choose_angle(): return round(random() * 360)



# letters = generate_letters()
# axiom = generate_axiom(letters)
# rules = generate_rules(letters)
# angle = choose_angle()
# drawn_variables = pick_drawn_variables(letters)

# print(axiom, rules)

def test(mat, r, c):
	i = 0
	j = 0
	new_mat = [[None for _ in range(c)] for _ in range(r)]

	for row in mat:
		for elem in row:
			new_mat[i][j] = elem
			j += 1
			if j == c:
				j = 0
				i += 1

	return new_mat if new_mat[-1][-1] != None else mat

print(test([[1, 2], [3, 4]], 2, 4))