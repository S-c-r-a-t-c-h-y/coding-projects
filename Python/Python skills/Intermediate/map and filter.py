ids = ['id1', 'id2', 'id22', 'id34','id100']

print(sorted(ids)) # alphabetical sorting
print(sorted(ids, key=lambda x: int(x[2:]))) # usage of a lambda function to specify a key for sorting


# the map function runs the function provided in the first parameter
# on every elements of the iterable provided as second argument
# and returns a generator
capital_ids = list(map(lambda x: x.title(), ids))
print(capital_ids)