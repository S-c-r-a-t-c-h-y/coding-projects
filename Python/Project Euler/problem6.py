sum1 = sum(i ** 2 for i in range(1, 101))
sum2 = sum(range(1, 101)) ** 2

print(sum2 - sum1)
