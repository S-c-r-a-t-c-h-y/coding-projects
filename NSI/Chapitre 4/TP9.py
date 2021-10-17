import time

def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

start = time.time()
n = int(input("fib(?) : "))
res = fib(n)
print(f"{fib(n) = }\nTemps d'exécution : {(time.time()-start):.5f}s")