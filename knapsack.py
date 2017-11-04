import itertools


def brute_force(n, m, weights, values):
    best_xs = [0, ] * n
    best_value = 0
    xss = itertools.product([0, 1], repeat=n)
    for xs in xss:
        total_value = 0
        total_weight = 0
        for x, weight, value in zip(xs, weights, values):
            total_value += value * x
            total_weight += weight * x
        if total_weight <= m and total_value > best_value:
            best_value = total_value
            best_xs = xs
    return best_value, best_xs


def brute_force_fn(n, m, weights, values):
    xss = itertools.product([0, 1], repeat=n)
    return max(
            [(sum([x * value for x, value in zip(xs, values)]),
                sum([x * weight for x, weight in zip(xs, weights)]),
                xs)
                for xs in xss],
            key=lambda args: (args[1] <= m, args[0])
            )


def heuristic(n, m, weights, values):
    xs = [0, ] * n
    total_value = 0
    total_weight = 0
    ratious = [value / weight for value, weight in zip(values, weights)]
    # sort according to value-weight ratio
    # if the ratio is the same prefer the lighter item
    for idx, (ratio, weight) in sorted(enumerate(zip(ratious, weights)),
                                       key=lambda x: (x[1][0], -x[1][1]),
                                       reverse=True):
        if total_weight + weight <= m:
            total_weight += weight
            total_value += values[idx]
            xs[idx] = 1
    return total_value, xs


def branch_and_bound(n, m, weights, values):
    best_value = 0

    def bb_recursive(value, n, m):
        nonlocal best_value  # look in nearest enclosing scope
        best_value = max(best_value, value)  # update best_value
        # check if this branch can improve value more than best_value
        if value + sum(values[:n]) <= best_value:
            return 0
        # base case
        if n == 0 or m <= 0:
            return 0
        # cannot fit the thing into knapsack
        if m < weights[n - 1]:
            return bb_recursive(value, n - 1, m)
        # try with and without the n - 1st thing
        return max(values[n - 1] + bb_recursive(value + values[n - 1], n - 1,
                                                m - weights[n - 1]),
                   bb_recursive(value, n - 1, m))

    return bb_recursive(0, n, m)


def read_instances(f):
    data = {}
    for line in f.readlines():
        # separator is whitespace and convert to integers
        items = list(map(int, line.split()))
        # key is id
        data[items[0]] = {
                'n': items[1],  # number of items
                'm': items[2],  # capacity
                'weights': items[3::2],  # items weights
                'values': items[4::2]  # items values
                }
    return data
