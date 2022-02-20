def permute(n: int):
    nums = list(range(n))
    permutation = "".join(map(str, nums))
    print(permutation)


permute(10)
