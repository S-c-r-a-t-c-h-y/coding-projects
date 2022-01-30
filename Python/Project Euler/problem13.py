sum = 0
with open("problem13.txt", "r") as f:
    for line in f.readlines():
        sum += int(line)

print(sum)
print(str(sum)[:10])
