import unittest
import sys
from test_cases import *

sys.path.append("..")
from constants import *

sys.path.append("../../src/ib110hw_testing")
from transformation.transformation import minimize, canonize


class TestMinimization(unittest.TestCase):
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

    def test_one_nondistinguishable(self):
        actual = canonize(minimize(one_nondistinguishable))
        expected = canonize(one_nondistinguishable_expected)
        self.are_valid(expected, actual)

    def test_two_nondistinguishable(self):
        actual = canonize(minimize(two_nondistinguishable))
        expected = canonize(two_nondistinguishable_expected)
        self.are_valid(expected, actual)

    def test_random(self):
        actual = canonize(minimize(random))
        expected = canonize(random_expected)
        self.are_valid(expected, actual)

    def test_random2(self):
        actual = canonize(minimize(random2))
        expected = canonize(random2_expected)
        self.are_valid(expected, actual)

    def test_three_nondistinguishable(self):
        actual = canonize(minimize(three_nondistinguishable))
        expected = canonize(three_nondistinguishable_expected)
        self.are_valid(expected, actual)

    def test_minimal1(self):
        actual = canonize(minimize(minimal))
        expected = canonize(minimal_expected)
        self.are_valid(expected, actual)

    def test_minimal2(self):
        actual = canonize(minimize(minimal2_expected))
        expected = canonize(minimal2_expected)
        self.are_valid(expected, actual)

    def test_two_equivalent_states(self):
        actual = canonize(minimize(two_equivalent_states))
        expected = canonize(two_equivalent_states_expected)
        self.are_valid(expected, actual)

    def test_disjoint(self):
        actual = canonize(minimize(disjoint))
        expected = canonize(disjoint_expected)
        self.are_valid(expected, actual)

    def test_empty_language_with_final_states_transitions(self):
        actual = canonize(minimize(empty_language_with_final_states))
        expected = canonize(empty_language_with_final_states_expected)
        self.are_valid(expected, actual)


if __name__ == "__main__":
    unittest.main()
