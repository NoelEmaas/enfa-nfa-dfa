from convert.nfa_to_dfa import NfaToDfaConverter


def main():
    inputs = input("Enter input symbols (separated by white spaces): ").split()
    states = input("Enter states (separated by white spaces): ").split()
    start_state = input("Enter start state: ")
    final_states = input("Enter accepting state/s (separated by white spaces): ").split()

    nfa_transition_table = get_nfa_transition_table(inputs, states)

    converter = NfaToDfaConverter()
    converter.convert(inputs, states, start_state, final_states, nfa_transition_table, "lazy")


def get_nfa_transition_table(inputs, states):
    nfa_transition_table = {state: {} for state in states}
 
    for i in inputs:
        print("Enter the set of states that can be reached from state q following only arcs labeled", input)
        for s in states:
            print(s, "-> ", end = "")
            output_states = input().split()
            nfa_transition_table[s][i] = output_states

    return nfa_transition_table


if __name__ == "__main__":
    main()
