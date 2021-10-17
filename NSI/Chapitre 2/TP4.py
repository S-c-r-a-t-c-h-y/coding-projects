def fib(n):
    """ fonction récursive qui retourne la valeur
    de la suite de fibonacci au rang n """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fib(n-1) + fib(n-2)

for i in range(21):
    print(f'fib({i}) = {fib(i)}')