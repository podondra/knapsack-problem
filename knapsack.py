import click
import itertools


def brute_force(n, m, weights, values):
    best_xs = (0, ) * n
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


def heuristic():
    ...


def read_instances(f):
    data = {}
    for line in f.readlines():
        # separator is whitespace and convert to integers
        items = list(map(int, line.split()))
        # key is id
        data[items[0]] = {
                'n': items[1],  # number of items
                'm': items[2],  # capacity
                'weights': items[3::2], # items weights
                'values': items[4::2]  # items values
                }
    return data


@click.command()
@click.argument('infile', type=click.File())
def knapsack(infile):
    instances = read_instances(infile)
    for i, inst in instances.items():
        solution = brute_force_fn(inst['n'], inst['m'],
                inst['weights'], inst['values'])
        print(i, inst['n'], solution[0], '', ' '.join(map(str, solution[2])))


if __name__ == '__main__':
    knapsack()
