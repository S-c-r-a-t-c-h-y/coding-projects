n = 2520

while not all(n % i == 0 for i in range(1, 20)):
    n += 2

print(n)
