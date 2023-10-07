from itertools import chain, combinations
from tabulate import tabulate

class NfaToDfaConverter:
    def __init__(self):
        self.dfa_transition_table = None
        self.nfa_transition_table = None
        self.inputs = None
        self.states = None
        self.method = None

    def convert(self, inputs, states, nfa_transition_table, method):
        self.nfa_transition_table = nfa_transition_table
        self.inputs = inputs
        self.states = states

        if method == "subset_construction":
            self._convert_using_subset_construction_method()
        if method == "lazy":
            self._convert_using_lazy_method()

    def _convert_using_subset_construction_method(self):
        powerset = self._create_powerset(self.states)
        powerset.append(set())

        self.dfa_transition_table = [[None] * len(self.inputs) for i in range(pow(2, len(self.states)))]

        for i in range(len(powerset)):
            sstates = powerset[i]
            for j in range(len(self.inputs)):
                curr_input = self.inputs[j]
                output_states = []
                for state in sstates:
                    output_states += self.nfa_transition_table[self.states.index(state)][self.inputs.index(curr_input)]
                self.dfa_transition_table[i][j] = set(sorted(set(output_states)))

        for i in range(len(self.dfa_transition_table)):
            self.dfa_transition_table[i].insert(0, powerset[i])

        self._print_dfa_transition_table()

    def _convert_using_lazy_method(self):
        pass

    def _create_powerset(self, q):
        powerset = chain.from_iterable(combinations(q, r) for r in range (1, len(q) + 1))
        return list(map(set, powerset))
        
    def _print_dfa_transition_table(self):
        print("\nDFA Transition Table:")
        print(tabulate(self.dfa_transition_table, headers = self.inputs, tablefmt='fancy_grid'))

