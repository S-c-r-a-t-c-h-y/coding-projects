def fib(n):
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)


sum = 0
n = 1
while (res := fib(n)) < 4_000_000:
    if res % 2 == 0:
        sum += res
    n += 1

print(sum)
