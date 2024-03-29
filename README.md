This library was created for the course **IB110 - Introduction to Informatics** at [MUNI FI](https://www.fi.muni.cz/). It builds on top of the [ib110hw](https://pypi.org/project/ib110hw/) and the [hypothesis](https://pypi.org/project/hypothesis/) libraries.

# Setup

Python version required for this library is **>=3.6**. It can be installed using `pip` like so:
```pip install ib110hw_testing```

Using venv to install the library is recommended as it has some dependencies (`ib110hw`, `exrex`, `hypothesis`).

# Modules

## Testing

The module `testing` contains some predefined strategies which can be used with the `hypothesis` library.

### Example Use-case

Below code shows a simple example of strategies used with tests.

```python
from hypothesis import given
from ib110hw.automaton.dfa import DFA
from ib110hw_testing.testing.strategies import dfas, strings_from_regex
from typing import Set

@given(
    dfas(alphabet={"a", "b", "c"}),
    strings_from_regex(regex="[abc]*")
)
def test(dfa: DFA, strings: Set[str])
    ...
```

## Transformation

The module `transformation` contains implementations of some algorithms which can be used to transform automata.

### Example Use-case

Below code shows a simple example of automata comparison.

```python
from ib110hw.automaton.dfa import DFA
from ib110hw.automaton.nfa import NFA
from ib110hw_testing.transformation.transformation import compare_automata

nfa: NFA = NFA(...) # an arbitrary NFA
dfa: DFA = DFA(...) # an arbitrary DFA

compare_automata(nfa, dfa) # returns True/False
```
