def f(n: int) -> int:
    """Returns n!"""
    return n * f(n - 1) if n != 1 else 1


print(sum(int(car) for car in str(f(100))))
