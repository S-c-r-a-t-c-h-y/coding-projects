from collections import *

'''
https://docs.python.org/fr/3/library/collections.html

datastructure in the collections module:
ChainMap
Counter
deque
defaultdict
namedtuple
OrderedDict

UserDict	|
UserList	| All of these help with class inheritance
UserString  |
'''

def ChainMapEx():
	dict1 = {1: 'one', 2: 'two'}
	dict2 = {2: 'three', 3: 'three', 4: 'foor'}
	dict3 = {'three': 3, 'foor': 4}

	chain = ChainMap(dict1, dict2, dict3)

	print(chain)
	print(chain.maps) # list containing each dictionnary of the map
	print(chain[2]) # research in every dict from start to end and returns the first matching value

	dict4 = {'one': 1, 'two': 2}
	chain2 = chain.new_child(dict4) # returns a new chainmap with the additional dict
	print(chain2)


def CounterEx():
	cnt = Counter() # empty Counter
	for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
		cnt[word] += 1
	print(cnt)

	c = Counter('abcbcbae') # from an iterable
	print(c)
	c = Counter({'red': 4, 'blue': 3, 'green': 1}) # from a mapping
	print(c)
	c = Counter(red=4, blue=2, green=1) # from kwargs
	print(c)

	c = Counter(['eggs', 'ham'])
	print(c['bacon'])

	c['eggs'] = 0 # doesn't delete it
	print(c)
	del c['eggs'] # deletes it
	print(c)

	c = Counter(a=4, b=2, c=0, d=-2)
	print(sorted(c.elements())) # .elements() returns an iterable

	print(Counter('abracadabra').most_common(3)) # returns the n most common key in the Counter

	c = Counter(a=4, b=2, c=0, d=-2)
	d = Counter(a=1, b=2, c=3, d=4)
	c.subtract(d) # substract from d, which can be an iterable or a Counter/dict
	print(c)
	print(+c) # removes 0 and negative counts

	c.update(a=2, b=3, c=4, d=2, e=1) # adds to the Counter
	print(c)

	c = Counter(a=3, b=1)
	d = Counter(a=1, b=2)

	print(c + d)         # add two counters together:  c[x] + d[x]
	print(c - d)         # subtract (keeping only positive counts)
	print(c & d)         # intersection:  min(c[x], d[x]) 
	print(c | d)         # union:  max(c[x], d[x])



def dequeEx():
	
	'''
	A deque is a double ended queue meaning that you can
	add and remove elements from both ends of the queue.
	It is a subclass of a list wich means that you have
	similar methods
	'''


	d = deque()
	print(d)
	d = deque(['red', 'blue', 'green'])
	print(d)

	# you can add and remove elements from both end of the deque

	d.append('yellow') # appends to the right
	print(d)
	d.appendleft('brown') # appends to the left
	print(d)

	d.extend(['white', 'black']) #extends to the right
	print(d)
	d.extendleft(['purple', 'pink']) # extends to the left but reverses the input order
	print(d)

	print(d.pop())
	print(d)

	print(d.popleft())
	print(d)

	d.rotate(1) # right rotation
	print(d) 

	d.rotate(-1) # left rotation
	print(d)

	print(d.maxlen) # length limit

	d = deque('abc', 5) # limit length of 5
	print(d.maxlen)
	d.extend('def')
	print(d) # the first element got truncated because of the max length



def defaultdictEx():
	'''
	A defaultdict is a subclass of a dict

	collections.defaultdict([default_factory[, ...]])
	'''

	s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
	d = defaultdict(list) # list as default_factory
	for k, v in s:
	    d[k].append(v)

	print(sorted(d.items()))


	s = 'mississippi'
	d = defaultdict(int) # int as default factory
	for k in s:
	    d[k] += 1

	print(sorted(d.items()))

	s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
	d = defaultdict(set) # set as default factory
	for k, v in s:
	    d[k].add(v)

	print(sorted(d.items()))


	dd = defaultdict(list)

	# Accessing a missing key creates it and
	# initializes it using the default factory,
	# i.e. list() in this example:
	dd["dogs"].append("Rufus")
	dd["dogs"].append("Kathrin")
	dd["dogs"].append("Mr Sniffles")

	dd["dogs"]



def namedtupleEx():
	'''
	Returns a new sublass of tuple named typename.

	collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)
	'''
	
	Point = namedtuple('Point', 'x, y')
	p = Point(12, y=74)
	print(p[0])
	print(p.y)

	x, y = p
	print(x, y)
	print(repr(p))

	t = [41, 12]
	u = Point._make(t) # creating an instance of the namedtuple from an iterable
	print(u)
	print(u._asdict()) # Representing the object as an OrderedDict

	v = u._replace(x=31) # creates a new instance replacing the specified fields with their new value
	print(v)
	print(v._fields) # strings tuple with the name of every fields

	d = {'x': 11, 'y': 22}
	p = Point(**d) # converting a dict into a namedtuple
	print(p)


def OrderedDictEx():
	'''
	An OrderedDict is a subclass of a dict but got additional capacities of ordering.

	collections.OrderedDict([items])
	'''
	
	d = OrderedDict({1: 'one', 2: 'two', 3: 'three'})
	print(d)

	print(d.popitem()) # poping from the end (LIFO)
	print(d)
	print(d.popitem(last=False)) # poping from the begining (FIFO)
	print(d)

	d = OrderedDict({1: 'one', 2: 'two', 3: 'three'})
	print('\n', d)
	d.move_to_end(1) # moved the element to the right end
	print(d)
	d.move_to_end(3, last=False) # moved the element to the left end
	print(d, '\n')

	d1 = OrderedDict({1: 'one', 2: 'two', 3: 'three'})
	d2 = OrderedDict({2: 'two', 1: 'one', 3: 'three'})
	print(d1, '\n', d2)
	print(d1 == d2) # OrderedDict are sensible to the order of the elements whereas dicts aren't


#ChainMapEx()
#CounterEx()
#dequeEx()
#defaultdictEx()
#namedtupleEx()
#OrderedDictEx()