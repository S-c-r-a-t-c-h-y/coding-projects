with open("day3_input.txt", "r") as f:
    nums = [line.strip() for line in f.readlines()]
    nums_0 = nums.copy()

    for index in range(12):
        new_nums_0 = [num for num in nums_0 if num[index] == "0"]
        nums_0 = new_nums_0.copy()
        print(new_nums_0)
        if len(new_nums_0) == 1:
            break

    print(nums_0)
