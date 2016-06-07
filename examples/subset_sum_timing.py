import random
import time
from functools import partial
from itertools import takewhile
#from multiprocessing import Pool

from infection import subset_sum

def takeuntil(predicate, iterable):
    # takewhile(lambda x: x<5, [1,4,6,4,1]) --> 1 4
    for x in iterable:
        yield x
        if not predicate(x):
            break

def trial(trial_num, algo, sample_size, element_size, proportion):
    sample = [random.randint(0,element_size) for r in xrange(sample_size)]
    target = int(sum(sample) * proportion)
    start = time.clock()
    res = subset_sum.optimize(sample, target, algo=algo)
    return time.clock() - start

def repeat_trial(num_trials, algo, sample_size, element_size, proportion):
    partial_trial = partial(trial, algo=algo, sample_size=sample_size,
                             element_size=element_size, proportion=proportion)
    #pool = Pool(8)
    runnings = map(partial_trial, xrange(num_trials))
    return sum(runnings) / num_trials

def trial_sizes(algo, trials, element_size, proportion):
    sample_size = 100
    while True:
        #print "running", algo, sample_size
        yield repeat_trial(trials, algo, sample_size, element_size, proportion)
        sample_size *= 2

def execution_limit(duration):
    return lambda running: running <= duration

def test_algo(algo, element_size, proportion):
    num_trials = 1
    trials = trial_sizes(algo, num_trials, element_size, proportion)
    return list(takeuntil(execution_limit(1), trials))

def test_all_algos(element_size, proportion):
    algorithms = subset_sum.algorithms
    algorithms.remove("exact")
    for algo in algorithms:
        yield [algo] + map(str,test_algo(algo, element_size, proportion))

def create_report(element_size, proportion):
    for result in test_all_algos(element_size, proportion):
        print ", ".join(result)

if __name__ == "__main__":
    create_report(10, .2)
