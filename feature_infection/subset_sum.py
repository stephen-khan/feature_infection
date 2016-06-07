"""
Subset Sum
"""
import operator
import inspect


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


def _exact_psudopolynomial(seq, target, key=None):
    """Perform an exact search for a subset satisfying the subset sum
    optimization problem.  This function executes in O(len(seq) * target) time
    """
    partial_sums = [[(0, None)] * (target + 1) for _ in xrange(len(seq) + 1)]
    for j in xrange(1, len(seq) + 1):
        val = key(seq[j - 1]) if key else seq[j - 1]
        for weight_left in xrange(0, target + 1):
            if val > weight_left:
                partial_sums[j][weight_left] = (partial_sums[j - 1][weight_left][0], (j - 1, weight_left))
                continue
            partial_sums[j][weight_left] = max([
                (partial_sums[j - 1][weight_left][0], (j - 1, weight_left)),
                (val + partial_sums[j - 1][weight_left - val][0], (j - 1, weight_left - val))
            ], key=operator.itemgetter(0))

    def _get_partial(node):
        return partial_sums[node[0]][node[1]]

    current = (len(seq), target)
    subset = []
    total = _get_partial(current)[0]
    #print "Extracting subset"
    while _get_partial(current)[1]:
        #print current, "=>", _get_partial(current)[1]
        if current[1] != _get_partial(current)[1][1]:
            #print "Adding item", current[0], "val:", seq[current[0] - 1]
            subset.append(seq[current[0] - 1])
        current = _get_partial(current)[1]
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
    "psudopolynomial": _exact_psudopolynomial,
    "approximation": _approximation,
    "greedy": _greedy,
    "iterated_greedy": _iterated_greedy
}


ALGORITHMS = _ALGORITHM_DEFINITIONS.keys()


def optimize(seq, target, algo="greedy", error=.5, key=None):
    """Solve the subset sum optimization problem"""
    if algo not in _ALGORITHM_DEFINITIONS:
        raise ValueError("{} is not a valid algorithm selection.".format(algo))
    impl = _ALGORITHM_DEFINITIONS[algo]
    kwargs = {"key": key}
    if "error" in inspect.getargspec(impl).args:
        kwargs["error"] = error
    return impl(seq, target, **kwargs)
