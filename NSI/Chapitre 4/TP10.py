import time

values = {}
def fib(n):
    """ calcul la nième valeur de la suite de fibonacci """
    
    if n in values:
        return values[n]
    if n <= 1:
        v = n
    else:
        v = fib(n-2) + fib(n-1)
    values[n] = v
    return v

start = time.time()
n = int(input("fib(?) : "))
res = fib(n)
print(f"fib({n}) = {fib(n)}\nTemps d'exécution : {(time.time()-start):.10f}s")
#print(f"Values : {values}")