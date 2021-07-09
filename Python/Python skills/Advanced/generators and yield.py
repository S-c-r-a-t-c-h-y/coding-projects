'''
The yield keyword is used to create a generator object.
It has to be used in a function.
The function itself turns into a generator that you can iterate throw
'''
from typing import Generator, Iterator



def infinite_sequence() -> Generator[int, None, None]:
    num = 0
    while True:
        yield num
        num += 1


for n in infinite_sequence():
    print(n)
    if n >= 200000:
        break

nums_squared_lc: list = [num ** 2 for num in range(5)] # list
nums_squared_gc: Iterator[int] = (num ** 2 for num in range(5)) # generator

# generator objects are way less 'memory expensive' than lists
print(nums_squared_lc)
print(nums_squared_gc)

# you can use the 'next' function to step throw the generator
print(next(nums_squared_gc))
print(next(nums_squared_gc))
print(next(nums_squared_gc))
print(next(nums_squared_gc))


def is_palindrome(num: int) -> bool:
    # Skip single-digit inputs
    if num // 10 == 0:
        return False
    temp: int = num
    reversed_num: int = 0

    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10

    if num == reversed_num:
        return True
    else:
        return False


def infinite_palindromes() -> Generator[int, int, None]:
    num: int = 0
    while True:
        if is_palindrome(num):
            i: int = (yield num)
            if i is not None:
                num = i
        num += 1


pal_gen = infinite_palindromes()
for i in pal_gen:
    print(i)
    digits = len(str(i))
    '''
    if digits == 5:
        pal_gen.throw(ValueError("We don't like large palindromes")) # throws an error
    '''
    if digits == 5:
        pal_gen.close() # stops any iteration from happening
        
    pal_gen.send(10 ** (digits)) #i gets the value
    
