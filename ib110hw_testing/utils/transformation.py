from copy import deepcopy
from typing import Union, Set, Deque, Dict, List
from ib110hw.automaton.nfa import NFA, NFATransitions
from ib110hw.automaton.dfa import DFA, DFATransitions
from collections import deque


def determinize(automaton: NFA) -> DFA:
    """
    Returns equivalent DFA version of the provided NFA using the powerset construction.
    Input automaton is not altered.

    Args:
        automaton (NFA): NFA automaton to be determinized

    Returns:
        DFA: Determinized automaton
    """
    automaton = remove_empty_transitions(automaton)

    states: Deque[Set[str]] = deque()
    states.append({automaton.initial_state})

    det_states: Set[str] = set()
    det_final_states: Set[str] = set()
    det_transitions = {automaton.initial_state: {}}

    while states:
        state = states.popleft()
        str_state = "".join(sorted(state))

        if str_state in det_states:
            continue

        det_states.add(str_state)
        det_transitions[str_state] = {}

        if automaton.final_states.intersection(state):
            det_final_states.add(str_state)

        for key in automaton.alphabet:
            new_state = set()
            for s in state:
                new_state = new_state | automaton.get_transition(s, key)

            if not new_state:
                new_state = {"sink"}

            det_transitions[str_state][key] = "".join(sorted(new_state))
            states.append(new_state)

    print(det_transitions)

    return DFA(
        states=det_states,
        alphabet=automaton.alphabet,
        final_states=det_final_states,
        initial_state=automaton.initial_state,
        transitions=det_transitions,
    )


def remove_empty_transitions(automaton: NFA) -> NFA:
    """
    Removes all epsilon (ε) transitions.
    Input automaton is not altered.

    Args:
        automaton (NFA): Automaton to be updated

    Returns:
        NFA: Equivalent automaton without ε transitions.
    """

    result: NFA = NFA(
        {*automaton.states},
        automaton.alphabet.difference({""}),
        automaton.initial_state,
        {*automaton.final_states},
        {},
    )

    if "" not in automaton.alphabet:
        result.transitions = deepcopy(automaton.transitions)
        return result

    next1: Dict[str, Set[str]] = {}

    # next1
    for state in automaton.states:
        next1[state] = {state} | automaton.get_transition(state, "")

        for next_state in automaton.get_transition(state, ""):
            next1[state] = next1[state] | next1.get(next_state, set())

    # next2
    for state in next1:
        for symbol in result.alphabet:
            for next_state in next1[state]:
                result.add_transition(
                    state, automaton.get_transition(next_state, symbol), symbol
                )

    # next3
    for state in result.transitions:
        for symbol in result.alphabet:
            next2_transition = {*result.get_transition(state, symbol)}

            for next_state in next2_transition:
                result.add_transition(state, next1.get(next_state, set()), symbol)

    return result


def remove_unreachable_states(automaton: Union[DFA, NFA]) -> Union[NFA, DFA]:
    """
    Removes unreachable states from the provided automaton.
    Input automaton is not altered.

    Args:
        automaton (Union[DFA, NFA]):

    Returns:
        Equal automaton without unreachable states.
    """
    result = deepcopy(automaton)
    reachable = {automaton.initial_state}
    queue = deque()

    queue.append(automaton.initial_state)

    while queue:
        state = queue.popleft()

        if isinstance(automaton, NFA):
            next_s = set()
            for symbol in automaton.alphabet:
                next_s.update(automaton.get_transition(state, symbol))
        else:
            next_s = {
                automaton.get_transition(state, symbol) for symbol in automaton.alphabet
            }

        queue.extend(next_s.difference(reachable))
        reachable.update(next_s)

    for state in list(automaton.states.difference(reachable)):
        result.remove_state(state)

    return result


# consider refactor/rewrite
def minimize(automaton: DFA) -> DFA:
    """
    Returns a minimized version of the provided automaton.
    Input automaton is not altered.

    Args:
        automaton (FA): Automaton to be minimized

    Returns:
        DFA: Minimized version of the provided automaton.
    """

    def get_groups(_transitions: DFATransitions) -> List[Set[str]]:
        """
        Divides states into equivalence groups based on the current
        transitions state
        """
        new_groups = {}

        for g_index, _group in enumerate(groups):
            for _state in sorted(_group):

                # group key is prefixed with index
                # to distinguish the same transitions from different groups
                group_key = f"{g_index}_"

                if _state not in _transitions.keys():
                    continue

                for _symbol in automaton.alphabet:
                    if _symbol not in _transitions[_state].keys():
                        continue

                    if transition := _transitions[_state][_symbol]:
                        group_key += transition

                if group_key not in new_groups.keys():
                    new_groups[group_key] = set()

                new_groups[group_key].add(_state)

        return [new_groups[key] for key in sorted(new_groups.keys())]

    minimized_transitions: DFATransitions = {}
    det_automaton: DFA = determinize(remove_unreachable_states(automaton))

    result: DFA = DFA(
        det_automaton.states,
        det_automaton.alphabet,
        det_automaton.initial_state,
        set(),
        minimized_transitions,
    )

    groups: List[Set[str]] = [
        det_automaton.final_states,
        det_automaton.states.difference(det_automaton.final_states),
    ]

    while True:
        # create transitions with group indexes instead of states
        # break when nothing changes
        marked_transitions = {}

        for state in det_automaton.transitions:
            for symbol in sorted(det_automaton.alphabet):
                for index, group in enumerate(groups):
                    if det_automaton.get_transition(state, symbol) not in group:
                        continue

                    if state not in marked_transitions.keys():
                        marked_transitions[state] = {}

                    marked_transitions[state][symbol] = f"{index}"

        prev_len = len(groups)
        groups = get_groups(marked_transitions)

        if prev_len == len(groups):
            break

    result.states = {f"{i}" for i in range(len(groups))}

    for index in range(len(groups)):
        if groups[index].intersection(det_automaton.final_states):
            result.final_states.add(f"{index}")

        if det_automaton.initial_state in groups[index]:
            result.initial_state = f"{index}"

        minimized_transitions[f"{index}"] = marked_transitions[groups[index].pop()]

    return result


def canonize(automaton: DFA) -> DFA:
    """
    Transforms provided automaton to its canonical form.
    Input automaton is not altered.

    Args:
        automaton (DFA): Automaton to be canonized

    Returns:
        Canonical form of the provided automaton.
    """
    renamed = {}
    states = deque()
    states.append(automaton.initial_state)

    # used for renaming the states
    # name is assigned based on the order the state was found
    # from the initial state
    rank = 0

    while states:
        current_state = states.popleft()

        if renamed.get(current_state, None):
            continue

        renamed[current_state] = f"{rank}"

        for symbol in sorted(automaton.alphabet):
            next_state = automaton.get_transition(current_state, symbol)

            if renamed.get(next_state, None):
                continue

            states.append(next_state)

        rank += 1

    renamed_transitions = {
        renamed[state]: deepcopy(automaton.transitions[state])
        for state in automaton.transitions.keys()
    }

    for state, value in renamed_transitions.items():
        for symbol in value.keys():
            prev = renamed_transitions[state][symbol]
            renamed_transitions[state][symbol] = renamed[prev]

    return DFA(
        {renamed[state] for state in automaton.states},
        {*automaton.alphabet},
        renamed[automaton.initial_state],
        {renamed[state] for state in automaton.final_states},
        renamed_transitions,
    )


def compare_automatons(a1: Union[NFA, DFA], a2: Union[NFA, DFA]) -> bool:
    if isinstance(a1, NFA):
        a1 = determinize(a1)

    if isinstance(a2, NFA):
        a2 = determinize(a2)

    a1 = canonize(minimize(a1))
    a2 = canonize(minimize(a2))

    return (
        a1.states == a2.states
        and a1.final_states == a2.final_states
        and a1.alphabet == a2.alphabet
        and a1.transitions == a2.transitions
    )


if __name__ == "__main__":
    pass
