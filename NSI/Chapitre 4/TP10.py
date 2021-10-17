import time

values = {}
def fib(n):
    """ calcul la nième valeur de la suite de fibonacci """
    
    if n <= 1:
        return n
    if n in values:
        return values[n]
    res = fib(n-2) + fib(n-1)
    values[n] = res
    return res

start = time.time()
n = int(input("fib(?) : "))
res = fib(n)
print(f"{fib(n) = }\nTemps d'exécution : {(time.time()-start):.10f}s")
#print(f"Values : {values}")