from decorators import *
import string
from typing import List


@exit_after(1)
def l(n):
	res = []
	for i in range(n):
		res.append(n*n)
	return res

@performance
def g(n):
	for i in range(n):
		yield n

l(10000000)
#g(10000000)
