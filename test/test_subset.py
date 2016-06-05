from .context import subset_sum
import pytest

subset_sum_algos = {
    "exact": lambda seq, target: subset_sum.exact(seq, target),
    "approximation": lambda seq, target: subset_sum.approximation(seq, target, .1),
    "greedy": lambda seq, target: subset_sum.greedy(seq, target),
}

@pytest.fixture(scope="session", params=subset_sum_algos.keys())
def algo(request):
    return subset_sum_algos[request.param]

class TestSubsetSumAlgorithm:
    def test_empty_set(self, algo):
        seq = []
        target = 1
        assert algo(seq, target) == (0, [])

    def test_complete_set(self, algo):
        seq = [1,2,3]
        target = 6
        assert subset_sum.exact(seq, target) == (6, [1,2,3])

    def test_larget_only(self, algo):
        seq = [1,2,3]
        target = 5
        assert subset_sum.exact(seq, target) == (5, [2,3])

    def test_target_larger_than_sum(self, algo):
        seq = [1,2,3]
        target = 7
        assert subset_sum.exact(seq, target) == (6, [1,2,3])

    def test_best_estimate(self, algo):
        seq = [2,3]
        target = 4
        assert subset_sum.exact(seq, target) == (3, [3])