"""
Subset Sum
"""
import operator
from itertools import takewhile


def _extend(seq, item):
    return [(weight + item, nodes + [item]) for weight, nodes in seq]


def _unique(seq, key=None):
    last_seen = None
    key = key or (lambda x: x)
    for item in seq:
        if last_seen != key(item):
            yield item


def _merge_list(seq1, seq2):
    key = operator.itemgetter(0)
    return list(_unique(sorted(seq1 + seq2, key=key), key=key))


def _accumulate_partials(seq, trim):
    partial_sums = [(0, [])]
    get_sum = operator.itemgetter(0)

    for item in seq:
        print partial_sums, "+", item, "=>",
        partial_sums = _merge_list(partial_sums, _extend(partial_sums, item))
        print partial_sums, "=>",
        partial_sums = trim(partial_sums, get_sum)
        print partial_sums
    return max(partial_sums, key=get_sum)


def exact(seq, target, key=None):
    """Perform an exact search for a subset satisfying the subset sum
    optimization problem.  This function executes in O(2^len(seq))
    """
    def trim_excess(seq, key):
        """Remove partial sums larger than target"""
        limit = lambda item: (key(item) if key else item) <= target
        return filter(limit, seq)
    return _accumulate_partials(seq, trim_excess)


def approximation(seq, target, error, key=None):
    """Polynomial time approximation to the subset sum optimization
    problem with tunable error.  This function executes in
    O(len(seq)**2 * ln(target) / error )
    """
    def trim(seq, key):
        """Remove partials larger than target or close to a smaller parial"""
        trimmed = [seq[0]]
        last = key(seq[0]) if key else seq[0]
        for item in seq[1:]:
            val = key(item) if key else item
            if val <= target and last < (1 - error / len(seq)) * val:
                trimmed.append(item)
                last = val
        return trimmed
    return _accumulate_partials(seq, trim)


def exact_psudopolynomial():
    """Perform an exact search for a subset satisfying the subset sum
    optimization problem.  This function executes in O(len(seq) * target) time
    """
    pass


def _sorted_greedy(sorted_seq, target, key):
    parial_sum = 0
    selected_subset = []
    for item in sorted_seq:
        val = key(item) if key else item
        if parial_sum + val <= target:
            parial_sum += val
            selected_subset.append(item)
    return (parial_sum, selected_subset)


def greedy(seq, target, key=None):
    """Find an approximate solution for the subset sum optimzation
    problem bounded by error of 1/2.  This function executes in
    O(len(seq)*log(n))
    """
    return _sorted_greedy(sorted(seq, reverse=True, key=key), target, key)


def iterated_greedy(seq, target, key=None):
    """Find an approximate solution to the subset sum optimation
    problem bounded by an error of 1/2.  This function executes in
    O(len(seq)**2)
    """
    seq = sorted(seq, reverse=True, key=key)
    greedy_sublists = (_sorted_greedy(seq[i:], target, key)
                       for i in xrange(len(seq)))
    return max(takewhile(greedy_sublists, lambda x: x != target), key=key)
