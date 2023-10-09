class Automaton:
    def __init__(self, transition_table, inputs, states, start_state, final_states):
        self.transition_table = transition_table
        self.inputs = inputs
        self.states = states
        self.start_state = start_state
        self.final_states = final_states

    