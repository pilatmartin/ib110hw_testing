from random import randint, choice, sample
from typing import Set, List
from ib110hw.automaton.dfa import DFA
from ib110hw.automaton.nfa import NFA
from utils.transformation import (
    automaton_to_graphviz,
    remove_unreachable_states,
    minimize,
    canonize,
    determinize,
)


def r_states(min_states: int, max_states: int) -> List[str]:
    return [f"s{i}" for i in range(randint(min_states, max_states))]


def r_dfa(
    min_deg: int,
    max_deg: int,
    min_states: int,
    max_states: int,
    min_fin_states: int,
    max_fin_states: int,
    alphabet: Set[str],
) -> DFA:
    """
    Generates random DFA:
        Generate random set of states (length between min_states and max_states)
        Pick an initial state from the generated set of states.

        For each state (starting with the initial state):
            Generate degree (between min_deg and max_deg)
            Generate set of next states (the amount depends on the generated degree)
            For every next state, pick a transition symbol

    Args:
        min_deg: The minimum degree of each state.
        max_deg: The maximum degree of each state.
        min_states: The minimum amount of states.
        max_states: The maximum amount of states.
        min_fin_states: The minimum amount of final states.
        max_fin_states: The maximum amount of final states.
        alphabet: Alphabet used by the automaton. (Not every symbol may be used)

    Returns:
        Random DFA. (Can be disjointed)
    """
    assert min_deg <= max_deg
    assert min_states <= max_states
    assert min_fin_states <= max_fin_states

    def add_next_states(_min_deg: int, _state: str) -> None:
        s_deg = randint(_min_deg, max_deg)
        next_states = sample(states, k=min(s_deg, len(states)))
        symbols = sample(list(alphabet), k=s_deg)

        for next_s, symbol in zip(next_states, symbols):
            result.add_transition(_state, next_s, symbol)

    # state degree cannot be bigger than the size of DFA automatons alphabet
    max_deg = min(len(alphabet), max_deg)
    min_deg = min(min_deg, max_deg)

    states = r_states(min_states, max_states)

    result = DFA(
        set(states),
        alphabet,
        choice(states),
        set(
            sample(
                states,
                k=randint(
                    min(len(states), min_fin_states), min(len(states), max_fin_states)
                ),
            )
        ),
        {state: {symbol: state for symbol in alphabet} for state in states},
    )

    add_next_states(1, result.initial_state)

    for state in result.states.difference([result.initial_state]):
        add_next_states(min_deg, state)

    return result


def r_nfa(
    min_deg: int,
    max_deg: int,
    min_states: int,
    max_states: int,
    min_fin_states: int,
    max_fin_states: int,
    alphabet: Set[str],
) -> NFA:
    """
    Generates random NFA:
        Generate random set of states (length between min_states and max_states)
        Pick an initial state from the generated set of states.

        For each state (starting with the initial state):
            Generate list of integers (sums up to the max_deg)->each integer is the amount of next states for a symbol.
            For each integer i, sample set of next states of size i.
            Add symbol to every sampled set.

    Args:
        min_deg: The minimum degree of each state.
        max_deg: The maximum degree of each state.
        min_states: The minimum amount of states.
        max_states: The maximum amount of states.
        min_fin_states: The minimum amount of final states.
        max_fin_states: The maximum amount of final states.
        alphabet: Alphabet used by the automaton. (Not every symbol may be used)

    Returns:
        Random NFA. (Can be disjointed)
    """

    def add_next_states(_min_deg: int, _max_deg: int, _state: str) -> None:
        s_deg = randint(_min_deg, max_deg)
        next_states = sample(states, k=min(s_deg, len(states)))

        for next_state in next_states:
            result.add_transition(_state, {next_state}, choice(list(alphabet)))

    states = [f"s{i}" for i in range(randint(min_states, max_states))]
    result = NFA(
        set(states),
        alphabet,
        choice(states),
        set(
            sample(
                states,
                k=randint(
                    min(len(states), min_fin_states), min(len(states), max_fin_states)
                ),
            )
        ),
        {},
    )

    add_next_states(1, max_deg, result.initial_state)

    for state in result.states.difference([result.initial_state]):
        add_next_states(min_deg, max_deg, state)

    return result


if __name__ == "__main__":
    r_dfa_automaton = r_dfa(
        min_deg=2,
        max_deg=3,
        min_states=3,
        max_states=8,
        min_fin_states=1,
        max_fin_states=3,
        alphabet={"a", "b", "c", "d"},
    )
    print(r_dfa_automaton)
    r_dfa_reachable = remove_unreachable_states(r_dfa_automaton)
    print(r_dfa_reachable)

    print(r_dfa_min := minimize(r_dfa_reachable))
    print(r_dfa_can := canonize(r_dfa_min))

    r_nfa_automaton = r_nfa(
        min_deg=2,
        max_deg=4,
        min_states=10,
        max_states=20,
        min_fin_states=5,
        max_fin_states=10,
        alphabet={"a", "b", "c", "d"},
    )
    print(r_nfa_automaton)
    r_nfa_reachable = remove_unreachable_states(r_nfa_automaton)
    print(r_nfa_reachable)

    r_nfa_determinized = determinize(r_nfa_automaton)

    # r_name = f"r_dfa_{randint(0, 10 ** 10)}"
    # automaton_to_graphviz(r_dfa_automaton, f"C:\\Skola\\SBAPR\\r_automatons\\r_dfa\\{r_name}.dot")
    # automaton_to_graphviz(r_dfa_reachable, f"C:\\Skola\\SBAPR\\r_automatons\\r_dfa\\{r_name}_reach.dot")
    # automaton_to_graphviz(r_dfa_min, f"C:\\Skola\\SBAPR\\r_automatons\\r_dfa\\{r_name}_min.dot")
    # automaton_to_graphviz(r_dfa_can, f"C:\\Skola\\SBAPR\\r_automatons\\r_dfa\\{r_name}_can.dot")
    #
    r_name = f"r_nfa_{randint(0, 10 ** 10)}"
    automaton_to_graphviz(
        r_nfa_automaton, f"C:\\Skola\\SBAPR\\r_automatons\\r_nfa\\{r_name}.dot"
    )
    automaton_to_graphviz(
        r_nfa_reachable, f"C:\\Skola\\SBAPR\\r_automatons\\r_nfa\\{r_name}_reach.dot"
    )
    automaton_to_graphviz(
        r_nfa_determinized, f"C:\\Skola\\SBAPR\\r_automatons\\r_nfa\\{r_name}_det.dot"
    )

    # to_minimize_t = {
    #     "A": {
    #         "a": "B",
    #         "b": "C",
    #     },
    #     "B": {
    #         "a": "D",
    #         "b": "E",
    #     },
    #     "C": {
    #         "a": "C",
    #         "b": "C",
    #     },
    #     "D": {
    #         "a": "B",
    #         "b": "E",
    #     },
    #     "E": {
    #         "a": "F",
    #         "b": "E",
    #     },
    #     "F": {
    #         "a": "G",
    #         "b": "E",
    #     },
    #     "G": {
    #         "a": "D",
    #         "b": "E",
    #     },
    # }
    #
    # to_minimize_a = DFA(
    #     {"A", "B", "C", "D", "E", "F", "G"},
    #     {"a", "b"},
    #     "A",
    #     {"B", "D", "F", "G"},
    #     to_minimize_t
    # )
    #
    # to_minimize_t2 = {
    #     "1": {
    #         "a": "2",
    #         "b": "4",
    #     },
    #     "2": {
    #         "a": "4",
    #         "b": "3",
    #     },
    #     "3": {
    #         "a": "3",
    #         "b": "6",
    #     },
    #     "4": {
    #         "a": "4",
    #         "b": "5",
    #     },
    #     "5": {
    #         "a": "5",
    #         "b": "5",
    #     },
    #     "6": {
    #         "a": "2",
    #         "b": "5",
    #     },
    # }
    #
    # to_minimize_a2 = DFA(
    #     {"1", "2", "3", "4", "5", "6"},
    #     {"a", "b"},
    #     "1",
    #     {"3", "5"},
    #     to_minimize_t2
    # )
    #
    # to_minimize_t3 = {
    #     "A": {
    #         "a": "B",
    #         "b": "D",
    #     },
    #     "B": {
    #         "a": "D",
    #         "b": "C",
    #     },
    #     "C": {
    #         "a": "C",
    #         "b": "F",
    #     },
    #     "D": {
    #         "a": "D",
    #         "b": "E",
    #     },
    #     "E": {
    #         "a": "E",
    #         "b": "E",
    #     },
    #     "F": {
    #         "a": "B",
    #         "b": "E",
    #     },
    # }
    #
    # to_minimize_a3 = DFA(
    #     {"A", "B", "C", "D", "E", "F"},
    #     {"a", "b"},
    #     "A",
    #     {"C", "E"},
    #     to_minimize_t3
    # )
    #
    # print(canonize(minimize(to_minimize_a)))
    # # print(to_minimize_a2)
    # print(canonize(minimize(to_minimize_a2)))
    # # print(minimize_2(to_minimize_a2))
    # print(canonize(minimize(to_minimize_a3)))
    #
    # to_minimize_t4 = {
    #     "1": {
    #         "a": "2",
    #         "b": "4",
    #     },
    #     "2": {
    #         "a": "4",
    #         "b": "3",
    #     },
    #     "3": {
    #         "a": "3",
    #         "b": "3",
    #     },
    #     "4": {
    #         "a": "4",
    #         "b": "5",
    #     },
    #     "5": {
    #         "a": "5",
    #         "b": "5",
    #     },
    #     "6": {
    #         "a": "6",
    #         "b": "5",
    #     }
    # }
    #
    # to_minimize_a4 = DFA(
    #     {"1", "2", "3", "4", "5", "6"},
    #     {"a", "b"},
    #     "1",
    #     {"3", "5"},
    #     to_minimize_t4
    # )
    #
    # automaton_to_graphviz(to_minimize_a4, f"C:\\Skola\\SBAPR\\r_automatons\\r_dfa\\to_minimize_a4.dot")
    # automaton_to_graphviz(minimize(to_minimize_a4), f"C:\\Skola\\SBAPR\\r_automatons\\r_dfa\\minimized_a4.dot")
