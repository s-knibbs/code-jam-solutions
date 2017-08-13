"""
Solution for the falling diamonds problem from
https://code.google.com/codejam/contest/2434486/dashboard#s=p

Solves both the small and large problems.
"""
import math
import sys

LEFT = 0
RIGHT = 1


def get_target_base_length(target):
    """
    Returns the base length of the
    smallest triangle that envelops coord
    """
    return abs(target[0]) + 1 + target[1]


def triangular(n):
    return n * (n + 1) // 2


def triangular_sequence():
    """
    Triangular number generator, starting at n==1
    """
    base = 1
    while True:
        yield (triangular(base), base)
        # Skip even base lengths
        base += 2


def count_where(predicate, iterable):
    """
    Count the number of items in iterable that satisfy
    the predicate
    """
    return sum(1 for x in iterable if predicate(x))


def multiset_permutations(word, alphabet=(LEFT, RIGHT)):
    """
    Calculates the number of permutations of the given multiset.
    See https://en.wikipedia.org/wiki/Permutation#Permutations_of_multisets
    """
    factorial_counts = [
        math.factorial(count_where(lambda x: x == symbol, word))
        for symbol in alphabet
    ]
    permutations = math.factorial(len(word))
    for f in factorial_counts:
        permutations //= f
    return permutations


def calculate_target_permutations(pivot, n, target, total_permutations):
    target_side, other_side = (LEFT, RIGHT) if target[0] < 0 else (RIGHT, LEFT)
    s = target[1]
    r = n - s
    # Not enough diamonds to reach the target
    if r < 0:
        return 0
    # Calculate permutations not containing the target
    # and subtract from the total
    invalid_permutations = 0
    while r <= pivot and s >= 0:
        target_word = [target_side] * s + [other_side] * r
        invalid_permutations += multiset_permutations(target_word)
        s -= 1
        r += 1
    return total_permutations - invalid_permutations


def calculate_probability(pivot, n, target):
    """
    Calculate the probability by finding all permutations containing
    the target divided by the total number of permutations of diamonds.
    Pivot is the maximum number of left or right falling diamonds allowed within
    each permutation.
    """
    diamond_permutations = 2**n
    # Subtract invalid permutations where left or right falling
    # diamonds exceeds the pivot
    for x in range(pivot + 1, n + 1):
        invalid_word = [LEFT] * x + [RIGHT] * (n - x)
        diamond_permutations -= 2 * multiset_permutations(invalid_word)
    target_permutations = calculate_target_permutations(pivot, n, target, diamond_permutations)
    return target_permutations / diamond_permutations


def solve(n, target):
    triangle, base = 0, 0
    # Get the smallest triangle that the diamonds will fit into
    for triangle, base in triangular_sequence():
        if n <= triangle:
            break
    target_base = get_target_base_length(target)
    if target_base > base:
        return 0.0
    elif target_base == base:
        # Enough diamonds to completely cover a triangle
        if n == triangle:
            return 1.0
        return calculate_probability(base - 1, n - triangular(base - 2), target)
    else:
        return 1.0


def read_input():
    num_cases = int(sys.stdin.readline().strip())
    for _ in range(num_cases):
        n, x, y = sys.stdin.readline().strip().split()
        yield (int(n), (int(x), int(y)))


if __name__ == "__main__":
    for idx, (diamonds, coord) in enumerate(read_input()):
        print("Case #%d: %.7f" % (idx + 1, solve(diamonds, coord)))
