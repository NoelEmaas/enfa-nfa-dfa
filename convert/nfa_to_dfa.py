from itertools import chain, combinations
from tabulate import tabulate

class NfaToDfaConverter:
    def __init__(self):
        self.dfa_transition_table = None
        self.nfa_transition_table = None
        self.inputs = None
        self.states = None
        self.start_state = None
        self.final_states = None
        self.method = None
        self.powerset = None

    def convert(self, inputs, states, start_state, final_states, nfa_transition_table, method):
        self.nfa_transition_table = nfa_transition_table
        self.inputs = inputs
        self.states = states
        self.start_state = start_state
        self.final_states = final_states
        self.dfa_transition_table = None

        if method == "subset_construction":
            self._convert_using_subset_construction_method()
        if method == "lazy":
            self._convert_using_lazy_method()

    def _convert_using_subset_construction_method(self):
        self.powerset = self._create_powerset(self.states)
        self.powerset.append(set())

        self.dfa_transition_table = {frozenset(state): {} for state in self.powerset}

        for set_of_states in self.powerset:
            for i in self.inputs:
                output_states = []
                for state in set_of_states:
                    output_states += self.nfa_transition_table[state][i]
                self.dfa_transition_table[frozenset(set_of_states)][i] = set(sorted(output_states))

        self._print_dfa_transition_table()

    def _convert_using_lazy_method(self):
        self.dfa_transition_table = [[None] * len(self.inputs) for i in range(len(self.states))]
        self.dfa_transition_table[0] = list(map(set, self.nfa_transition_table[0]))
        new_states = [self.start_state]
        curr_row = 0

        while len(new_states) > 0:
            curr_state = new_states.pop(0)
            for i in range(len(self.inputs)):
                curr_input = self.inputs[i]
                output_states = []
                for state in curr_state:
                    output_states += self.nfa_transition_table[self.states.index(state)][self.inputs.index(curr_input)]
                output_states = set(sorted(set(output_states)))
                if output_states not in new_states:
                    self.dfa_transition_table.append(output_states)
                    new_states.append(output_states)
                self.dfa_transition_table[curr_row][i] = output_states
            curr_row += 1
        
        self._print_dfa_transition_table()

    def _create_powerset(self, q):
        powerset = chain.from_iterable(combinations(q, r) for r in range (1, len(q) + 1))
        return list(map(set, powerset))
        
    def _print_dfa_transition_table(self):
        table_body = []
        for state in self.powerset:
            row = [state]
            for i in self.inputs:
                row += [self.dfa_transition_table[frozenset(state)][i]]
            table_body.append(row)

        print("\nDFA Transition Table:")
        print(tabulate(table_body, headers = self.inputs, tablefmt='fancy_grid'))

