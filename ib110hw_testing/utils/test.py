from transformation import determinize, minimize, canonize
from ib110hw.automaton.nfa import NFA, NFATransitions
from ib110hw.automaton.utils import automaton_to_graphviz

nfa_transitions: NFATransitions = {
    "s1": { 
        "1": { "s2" }, 
        "0": { "s4" }, 
    },
    "s2": { 
        "1": { "s3" }, 
    },
    "s4": { 
        "0": { "s3" }, 
    },
}

automaton = NFA(
    states={"s1", "s2", "s3", "s4", "s5" },
    alphabet={"1", "0"},
    initial_state="s1",
    final_states={"s3"},
    transitions=nfa_transitions,
)

min_automaton = minimize(automaton)
det_automaton = determinize(automaton)
can_automaton = canonize(min_automaton)

print(automaton)
print(det_automaton)
print(min_automaton)
# print(can_automaton)
automaton_to_graphviz(det_automaton, "./det_automaton.dot")
automaton_to_graphviz(min_automaton, "./min_automaton.dot")
automaton_to_graphviz(can_automaton, "./can_automaton.dot")
