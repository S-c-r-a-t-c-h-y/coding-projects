position = depth = aim = 0

with open("day2_input.txt", "r") as f:
    for line in f.readlines():
        action, amt = line.split(" ")
        if action == "forward":
            position += int(amt)
            depth += aim * int(amt)
        elif action == "down":
            aim += int(amt)
        elif action == "up":
            aim -= int(amt)

print(position, depth, position * depth)
