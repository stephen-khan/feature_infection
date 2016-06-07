from .context import subset_sum as ss
import pytest

@pytest.fixture(scope="session", params=ss.ALGORITHMS)
def algo(request):
    return request.param


def check_result(actual, expected, key=None):
    correct_value = actual[0] == expected[0]
    return correct_value and sorted(actual[1], key=key) == sorted(expected[1], key=key)


class TestSubsetSumAlgorithm:
    def test_empty_set(self, algo):
        seq = []
        target = 1
        assert check_result(ss.optimize(seq, target, algo=algo), (0, []))

    def test_complete_set(self, algo):
        seq = [1,2,3]
        target = 6
        assert check_result(ss.optimize(seq, target, algo=algo), (6, [1,2,3]))

    def test_larget_only(self, algo):
        seq = [1,2,3]
        target = 5
        assert check_result(ss.optimize(seq, target, algo=algo), (5, [2,3]))

    def test_target_larger_than_sum(self, algo):
        seq = [1,2,3]
        target = 7
        assert check_result(ss.optimize(seq, target, algo=algo), (6, [1,2,3]))

    def test_best_estimate(self, algo):
        seq = [2,3]
        target = 4
        assert check_result(ss.optimize(seq, target, algo=algo), (3, [3]))

    def test_optimize_with_key(self, algo):
        seq = [set(["a"]), set(["b", "c"]), set(["d", "e", "f"])]
        target = 5
        res = (5, seq[1:])
        assert check_result(ss.optimize(seq, target, key=len, algo=algo), res, key=len)