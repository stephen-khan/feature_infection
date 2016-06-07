import random
import time
from functools import partial
from itertools import groupby, imap
from operator import itemgetter
from collections import namedtuple, defaultdict
#from multiprocessing import Pool

from feature_infection import subset_sum

# An implementation of execut solution to subset sum optimization that returns
# only the sum, not the subset itself.  The real version runs out of memory
# between 30 and 100 elements.
def unique_justseen(iterable, key=None):
    "List unique elements, preserving order. Remember only the element just seen."
    return map(next, imap(itemgetter(1), groupby(iterable, key)))

def extend(L, x):
    return map(lambda l: l + x, L)

def merge_list(U, V):
    return unique_justseen(sorted(U+V))

def exact(S, t):
    n = len(S)
    L = [0]
    for i in xrange(n):
        #print L, ",", S[i], "->",
        L = merge_list(L, extend(L, S[i]))
        L = filter(lambda l: l <= t, L)
        #print L
    return max(L)


TestData = namedtuple("TestData", ["samples", "target"])
def create_test_data(sample_size, element_size, proportion):
    sample = [random.randint(1,element_size) for r in xrange(sample_size)]
    target = int(sum(sample) * proportion)
    return TestData(sample, target)

def trial(algo, test_data):
    start = time.clock()
    if algo != "exact":
        res, _ = subset_sum.optimize(test_data.samples, test_data.target, algo=algo)
    else:
        res = exact(test_data.samples, test_data.target)
    return time.clock() - start, res

def get_report_data():
    active_algos = set(subset_sum.ALGORITHMS)
    sample_size = 100
    overtime = 10
    metadata = defaultdict(list)
    timings = defaultdict(list)
    results = defaultdict(list)

    while active_algos:
        metadata["sample_size"].append(sample_size)
        test_data = create_test_data(sample_size, 10, .2)
        metadata["target"].append(test_data.target)
        algos_overtime = set()
        for algo in active_algos:
            timing, result = trial(algo, test_data)
            timings[algo].append(timing)
            results[algo].append(result)
            if timing > overtime:
                algos_overtime.add(algo)
        sample_size *= 2
        active_algos ^= algos_overtime
    return metadata, timings, results


def create_report(metadata, timings, results):
    print ", ".join(["sample_size"] + map(str, metadata['sample_size']))
    for algo in subset_sum.ALGORITHMS:
        print ", ".join([algo] + map(str, timings[algo]))
    print
    print ", ".join(["target"] + map(str, metadata['target']))
    for algo in subset_sum.ALGORITHMS:
        print ", ".join([algo] + map(str, results[algo]))

if __name__ == "__main__":
    report_data = get_report_data()
    create_report(*report_data)
