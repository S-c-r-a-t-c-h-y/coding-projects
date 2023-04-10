import time

def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

start = time.time()
n = int(input("fib(?) : "))
res = fib(n)
print(f"fib({n}) = {fib(n)}\nTemps d'exécution : {(time.time()-start):.10f}s")