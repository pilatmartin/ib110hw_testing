import unittest
import sys
from test_cases import *

sys.path.append("..")
from constants import *

sys.path.append("../../src/ib110hw_testing")
from transformation.transformation import determinize, canonize


class TestDeterminization(unittest.TestCase):
    def are_valid(self, expected, actual):
        with self.subTest():
            self.assertEqual(expected.states, actual.states, INVALID_STATES)
            self.assertEqual(expected.alphabet, actual.alphabet, INVALID_ALPHABET)
            self.assertEqual(
                expected.initial_state, actual.initial_state, INVALID_INITIAL_STATE
            )
            self.assertEqual(
                expected.final_states, actual.final_states, INVALID_FINAL_STATES
            )
            self.assertEqual(
                expected.transitions, actual.transitions, INVALID_TRANSITIONS
            )

    def compare_and_test(self, a1, a2):
        actual = canonize(determinize(a1))
        expected = canonize(a2)
        self.are_valid(expected, actual)

    def test_lecture(self):
        self.compare_and_test(lecture_a, lecture_a_exp)

    def test_star(self):
        self.compare_and_test(star1_a, star1_a_exp)

    def test_star_equivalent_states(self):
        self.compare_and_test(star2_a, star2_a_exp)

    def test_star_every_other_accepting(self):
        self.compare_and_test(star3_a, star3_a_exp)

    def test_empty_to_only_accepting(self):
        self.compare_and_test(empty_to_acc_a, empty_to_acc_a_exp)

    def test_disjoint(self):
        self.compare_and_test(disjoint_a, disjoint_a_exp)

    def test_complete(self):
        self.compare_and_test(complete_a, complete_a_exp)


if __name__ == "__main__":
    unittest.main()
