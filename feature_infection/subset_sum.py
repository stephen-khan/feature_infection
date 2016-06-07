"""
Library for solving the subset sum optimization problem

This library has algorithms for solving the subset sum problem.
These include exact and approximation algorithms.

The subset sum optimation problem asks to find a subset with
the maximal sum that is no larger than a supplied target.  The
exact solution is NP-Complete so we default to a greedy algorithm
that is fast and works well in practice.

Exports:
    ALGORITHMS: list of implemented algorithms
    optimize: uses the algorithms to solve the subset sum problem
"""
from collections import namedtuple
import operator
import inspect
import logging


_LOG = logging.getLogger(__name__)


def _takeuntil(predicate, iterable):
    # takeuntil(lambda x: x<5, [1,4,6,4,1]) --> 1 4 5
    for item in iterable:
        yield item
        if not predicate(item):
            break


def _extend(seq, item, key=None):
    val = key(item) if key else item
    return [(weight + val, nodes + [item]) for weight, nodes in seq]


def _unique(seq, key=None):
    last_seen = None
    key = key or (lambda x: x)
    for item in seq:
        if last_seen != key(item):
            yield item


def _merge_list(seq1, seq2):
    key = operator.itemgetter(0)
    return list(_unique(sorted(seq1 + seq2, key=key), key=key))


def _accumulate_partials(seq, trim, key=None):
    partial_sums = [(0, [])]
    get_sum = operator.itemgetter(0)

    for item in seq:
        new_partials = _extend(partial_sums, item, key=key)
        partial_sums = _merge_list(partial_sums, new_partials)
        partial_sums = trim(partial_sums, get_sum)
    return max(partial_sums, key=get_sum)


def _exact(seq, target, key=None):
    """Perform an exact search for a subset satisfying the subset sum
    optimization problem.  This function executes in O(2^len(seq))
    """
    def trim_excess(seq, getsum):
        """Remove partial sums larger than target"""
        limit = lambda item: getsum(item) <= target
        return filter(limit, seq)
    return _accumulate_partials(seq, trim_excess, key=key)


def _approximation(seq, target, error, key=None):
    """Polynomial time approximation to the subset sum optimization
    problem with tunable error.  This function executes in
    O(len(seq)**2 * ln(target) / error )
    """
    def trim(seq, getsum):
        """Remove partials larger than target or close to a smaller parial"""
        trimmed = [seq[0]]
        last = getsum(seq[0])
        for item in seq[1:]:
            val = getsum(item)
            if val <= target and last < (1 - error / len(seq)) * val:
                trimmed.append(item)
                last = val
        return trimmed
    return _accumulate_partials(seq, trim, key=key)


def _psudopolynomial(seq, target, key=None):
    """Perform an exact search for a subset satisfying the subset sum
    optimization problem.  This function executes in O(len(seq) * target) time
    """
    # Create a dynamic programming matrix.  The format of each cell is a tuple
    # of maximum weight so far, and a pointer to the previous entry used.
    #pylint: disable=invalid-name
    PartialSum = namedtuple("PartialSum", ["sum", "last_used"])
    partial_sums = [[PartialSum(0, None)] * (target + 1)
                    for _ in xrange(len(seq) + 1)]

    def _get_partial(first_n, max_weight):
        return partial_sums[first_n][max_weight]

    def _use_previous(first_n, max_weight, val):
        previous = (first_n - 1, max_weight - val)
        return PartialSum(val + _get_partial(*previous).sum, previous)

    # Fill in values for the maximal partial sums using the first n elements
    # up to the given weight remaining
    for first_n in xrange(1, len(seq) + 1):
        val = key(seq[first_n - 1]) if key else seq[first_n - 1]
        for weight_left in xrange(0, target + 1):
            if val > weight_left:
                partial_sums[first_n][weight_left] = _use_previous(
                    first_n, weight_left, 0)
                continue
            partial_sums[first_n][weight_left] = max([
                _use_previous(first_n, weight_left, 0),
                _use_previous(first_n, weight_left, val)
            ], key=operator.itemgetter(0))

    # Use the previous pointers to walk back the matrix to determine which
    # elements were added to get the maximal sum.  We select by changes in
    # the sum.
    current = (len(seq), target)
    subset = []
    total = _get_partial(*current).sum
    while _get_partial(*current).last_used:
        # check the weight component of the last pointer
        if current[1] != _get_partial(*current).last_used[1]:
            subset.append(seq[current[0] - 1])
        current = _get_partial(*current).last_used
    return (total, subset)


def _sorted_greedy(sorted_seq, target, key):
    parial_sum = 0
    selected_subset = []
    for item in sorted_seq:
        val = key(item) if key else item
        if parial_sum + val <= target:
            parial_sum += val
            selected_subset.append(item)
    return (parial_sum, selected_subset)


def _greedy(seq, target, key=None):
    """Find an approximate solution for the subset sum optimzation
    problem bounded by error of 1/2.  This function executes in
    O(len(seq)*log(n))
    """
    return _sorted_greedy(sorted(seq, reverse=True, key=key), target, key)


def _iterated_greedy(seq, target, key=None):
    """Find an approximate solution to the subset sum optimation
    problem bounded by an error of 1/2.  This function executes in
    O(len(seq)**2)
    """
    if not seq:
        return (0, [])
    seq = sorted(seq, reverse=True, key=key)
    greedy_sublists = (_sorted_greedy(seq[i:], target, key)
                       for i in xrange(len(seq)))
    not_at_target = lambda x: x[0] != target
    get_sum = operator.itemgetter(0)
    return max(_takeuntil(not_at_target, greedy_sublists), key=get_sum)


_ALGORITHM_DEFINITIONS = {
    "exact": _exact,
    "psudopolynomial": _psudopolynomial,
    "approximation": _approximation,
    "greedy": _greedy,
    "iterated_greedy": _iterated_greedy
}


ALGORITHMS = _ALGORITHM_DEFINITIONS.keys()


def _invoke_algorithm(algo, seq, target, error, key):
    kwargs = {'key': key}
    # Approximation algorithms require an error parameter.  Add if required.
    if "error" in inspect.getargspec(algo).args:
        kwargs['error'] = error
    return algo(seq, target, **kwargs)


def optimize(seq, target, algo="greedy", error=.5, key=None):
    """Find a subset with the maximal sum bounded by target

    Solves the subset sum problem, either exactly or with an
    approximation algorithm.  The solver can use any of the
    algorithms in the subset sum package, but defaults to a
    greedy heuristic algorithm.  This default runs in O(n * log(n))
    time.

    Args:
        seq (list):  list of elements to optimize using the
            value or keyed value as the weight
        target (int): the limit of the returned subset sum
        algo (string): name of the algorithm to use. Defaults
            to greedy
        (optional) error (float): limits the error when searching for
            and approximate solution.  Only applicable to
            tunable approximation algorithms (like approximate).
            Defaults to .5
        (optional)key (function obj -> int): get weight of list
            item when present.  Otherwise, use the item itself.
            Defaults to None

    Returns:
        sum (int) * subset (list): returns a subset of the original
            items as a list.  Also provides the sum of the value of
            each of those items

    Raises:
        ValueError: algorithm is not one defined in ALGORITHMS package
            variable

    Exampes:
        >>> optimize([1,2,3], 5)
        (5, [2,3])

        >>> optimize([{"x": 1}, {"x": 2}, {"x": 3}], 5, algo="exact",\
key=operator.itemgetter("x"))
        (5, [{"x": 2}, {"x": 3}])
    """
    if algo not in _ALGORITHM_DEFINITIONS:
        raise ValueError("{} is not a valid algorithm selection.".format(algo))
    impl = _ALGORITHM_DEFINITIONS[algo]
    return _invoke_algorithm(impl, seq, target, error, key)

