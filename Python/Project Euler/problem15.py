computed = {}


def nb_route(n, m):
    """Returns the number of possible route in a n x m grid starting
    at the top-left corner going to the bottom-right corner while only
    moving right or down."""
    if n == 0 or m == 0:
        return 1

    if (n, m) in computed:
        return computed[(n, m)]

    res = nb_route(n - 1, m) + nb_route(n, m - 1)
    computed[(n, m)] = res
    return res


print(nb_route(20, 20))
