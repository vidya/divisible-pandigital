# https://projecteuler.net/problem=43
#
# Sub-string divisibility
# Problem 43
# The number, 1406357289, is a 0 to 9 pandigital number because it is
# made up of each of the digits 0 to 9 in some order, but it also has
# a rather interesting sub-string divisibility property.
#
# Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way,
# we note the following:
#
# d2d3d4=406 is divisible by 2
# d3d4d5=063 is divisible by 3
# d4d5d6=635 is divisible by 5
# d5d6d7=357 is divisible by 7
# d6d7d8=572 is divisible by 11
# d7d8d9=728 is divisible by 13
# d8d9d10=289 is divisible by 17
# Find the sum of all 0 to 9 pandigital numbers with this property.

from itertools import permutations, ifilter, imap
from functools import wraps
from time import time

import types


class DivisibilityFilter(object):
    PRIMES = [2, 3, 5, 7, 11, 13, 17]

    def __init__(self, func):
        self.func = func

    def prime_divisibility(self, perm):
        if (100 * perm[0 + 1] + 10 * perm[0 + 2] + perm[0 + 3]) % 2:
            return False

        if (100 * perm[1 + 1] + 10 * perm[1 + 2] + perm[1 + 3]) % 3:
            return False

        if (100 * perm[2 + 1] + 10 * perm[2 + 2] + perm[2 + 3]) % 5:
            return False

        for n in range(3, 7):
            if (100 * perm[n + 1] + 10 * perm[n + 2] + perm[n + 3]) % self.PRIMES[n]:
                return False

        return True

    def __get__(self, obj, objtype=None):
        return types.MethodType(self, obj, objtype)

    def __call__(self, *args, **kwargs):
        return ifilter(self.prime_divisibility, self.func(*args, **kwargs))


class DivisiblePandigital(object):
    @DivisibilityFilter
    def perms(self):
        return permutations(range(10))

    def divisible_perm_sum(self):
        return imap(lambda perm: reduce(lambda s, d: 10 * s + d, perm, 0),
                    self.perms())


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        ret_value = func(*args, **kwargs)
        end = time()

        time_taken = end - start
        return ret_value, time_taken

    return wrapper


@time_it
def calc_sum():
    return sum(DivisiblePandigital().divisible_perm_sum())

# main()
answer, time_taken = calc_sum()
print('(answer, time_taken): ({0}, {1})'.format(answer, time_taken))

