from tabulate import tabulate

class ENfaToNfaConverter:
    def __init__(self):
        self.enfa_transition_table = None
        self.nfa_transition_table = None
        self.inputs = None
        self.states = None
        self.start_state = None
        self.final_states = None
        self.method = None

    def convert(self, automaton):
        self.enfa_transition_table = automaton.transition_table
        self.inputs = automaton.inputs
        self.states = automaton.states
        self.start_state = automaton.start_state
        self.final_states = automaton.final_states
        self.nfa_transition_table = None

        for state in self.states:
            self.enfa_transition_table[state]['CL(q)'] = self._get_closure_states(state)
            for i in self.inputs:
                if i != 'ε':
                    self.enfa_transition_table[state]['S' + str(i)] = self._getS(i, state)

        for state in self.states:
            for i in self.inputs:
                if i != 'ε':
                    si_closure = []
                    si_states = self.enfa_transition_table[state]['S' + str(i)]
                    for si_state in si_states:
                        si_closure += self._get_closure_states(si_state)
                    self.enfa_transition_table[state]['δN(q,' + str(i) + ')'] = set(si_closure)

        self._print_nfa_transition_table(self.states)

    def _get_closure_states(self, state):
        closure_states = set()
        states_stack = [state]

        while (len(states_stack)):
            curr_state = states_stack.pop(0)
            if curr_state not in closure_states:
                closure_states.add(curr_state)
            for i in self.enfa_transition_table[curr_state]['ε']:
                if i not in closure_states:
                    states_stack.append(i)

        return closure_states

    def _getS(self, input, state):
        closure_states = self.enfa_transition_table[state]['CL(q)']
        s = []
        for state in closure_states:
            s += self.enfa_transition_table[state][input]
        return set(s)

    def _print_nfa_transition_table(self, states):
        headers = ['']
        for i in self.inputs:
            headers += [i]
        headers.append('CL(q)')
        for i in self.inputs:
            if i != 'ε':
                headers.append('S' + str(i))
        for i in self.inputs:
            if i != 'ε':
                headers.append('δN(q,' + str(i) + ')')
        
        table_body = []
        for state in states:
            row = [state]
            for i in self.inputs:
                row += [self.enfa_transition_table[state][i]]
            row += [self.enfa_transition_table[state]['CL(q)']]
            for i in self.inputs:
                if i != 'ε':
                    row += [self.enfa_transition_table[state]['S' + str(i)]]
            for i in self.inputs:
                if i != 'ε':
                    row += [self.enfa_transition_table[state]['δN(q,' + str(i) + ')']]
            table_body.append(row)

        print("\nENFA to NFA Transition Table:")
        print(tabulate(table_body, headers = headers, tablefmt='fancy_grid'))