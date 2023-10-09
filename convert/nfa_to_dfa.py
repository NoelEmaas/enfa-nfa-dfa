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

    def convert(self, automaton, method):
        self.nfa_transition_table = automaton.transition_table
        self.inputs = automaton.inputs
        self.states = automaton.states
        self.start_state = automaton.start_state
        self.final_states = automaton.final_states

        if method == 1:
            self._convert_using_subset_construction_method()
        if method == 2:
            self._convert_using_lazy_method()

    def _convert_using_subset_construction_method(self):
        powerset = self._create_powerset(self.states)
        powerset.append(set())

        self.dfa_transition_table = {frozenset(state): {} for state in powerset}

        for set_of_states in powerset:
            for i in self.inputs:
                output_states = []
                for state in set_of_states:
                    output_states += self.nfa_transition_table[state][i]
                self.dfa_transition_table[frozenset(set_of_states)][i] = set(sorted(output_states))

        self._print_dfa_transition_table(states = powerset)

    def _convert_using_lazy_method(self):
        self.dfa_transition_table = {}
        new_states = [{self.start_state}]
        created_states = []

        while len(new_states) > 0:
            curr_state = new_states.pop(0)
            self.dfa_transition_table[frozenset(curr_state)] = {}
            created_states.append(curr_state)
            for i in self.inputs:
                output_states = []
                for state in curr_state:
                    output_states += self.nfa_transition_table[state][i]
                output_states = set(sorted(output_states))
                if output_states not in created_states:
                    new_states.append(output_states)
                self.dfa_transition_table[frozenset(curr_state)][i] = output_states
        
        self._print_dfa_transition_table(states = created_states)

    def _create_powerset(self, q):
        powerset = chain.from_iterable(combinations(q, r) for r in range (1, len(q) + 1))
        return list(map(set, powerset))
        
    def _print_dfa_transition_table(self, states):
        table_body = []
        for state in states:
            row = [state]
            for i in self.inputs:
                row += [self.dfa_transition_table[frozenset(state)][i]]
            table_body.append(row)

        print("\nDFA Transition Table:")
        print(tabulate(table_body, headers = self.inputs, tablefmt='fancy_grid'))