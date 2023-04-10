''' python lambda functions are anonymous functions'''

square = lambda y: y ** 2 # used with one argument
#print(square(4))

full_name = lambda first, last: f'Full name : {first.title()} {last.title()}' # used with two args
#print(full_name('mazoyer', 'amaury'))

func_sum = lambda x, func: x + func(x)
#print(func_sum(-3, lambda x: x * x))

'''
overall lambda is very unpractical and it is most of the time
better to use normal functions defined with 'def'
'''