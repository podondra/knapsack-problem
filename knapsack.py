import itertools
import numpy


def brute_force(n, m, weights, values):
    best_xs = [0] * n
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
    xs = [0 ] * n
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
    best_xs, xs = None, [0] * n

    def bb_recursive(value, n, m):
        nonlocal best_value, best_xs, xs

        if best_value < value:
            best_value = value
            best_xs = xs[:]
        # check if this branch can improve value more than best_value
        if value + sum(values[:n]) <= best_value:
            return 0
        if n == 0 or m <= 0:
            return 0
        if m < weights[n - 1]:
            return bb_recursive(value, n - 1, m)
        xs[n - 1] = 1
        value_with = values[n - 1] + bb_recursive(value + values[n - 1],
                                                  n - 1, m - weights[n - 1])
        xs[n - 1] = 0
        value_without = bb_recursive(value, n - 1, m)
        return max(value_with, value_without)

    return bb_recursive(0, n, m), best_xs


def dynamic_programming(n, m, weights, values):
    # TODO implement forward phase
    max_value = sum(values)
    inf = numpy.iinfo(numpy.int32).max
    W = numpy.full((n + 1, max_value + 2), inf, dtype=numpy.int32)
    W[0, 0] = 0
    for i in range(n):
        for v in range(max_value + 1):
            # W[-1] contains inf
            W[i + 1, v] = min(W[i, v],
                              W[i, max(-1, v - values[i])] + weights[i])

    best_value = 0
    for value, weight in enumerate(W[-1]):
        if weight <= m and best_value < value:
            best_value = value

    best_xs = [0] * n
    value = best_value
    for i in range(n, -1, -1):
        if W[i - 1, value] != W[i, value]:
            value -= values[i - 1]
            best_xs[i - 1] = 1

    return best_value, best_xs


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
