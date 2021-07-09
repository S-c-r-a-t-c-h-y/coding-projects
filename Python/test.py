

K, M = 3, 1000

f = lambda x: x ** 2
s = lambda x: sum(map(f, x)) % 1000

lists = [[5, 4],
		 [7, 8, 9],
		 [5, 7, 8, 9, 10]]

for l in lists:
	l.sort()
picks = [None] * len(lists)

max = 0
