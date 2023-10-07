from convert.nfa_to_dfa import NfaToDfaConverter


def main():
    inputs = input("Enter input symbols (separated by white spaces): ").split()
    states = input("Enter states (separated by white spaces): ").split()
    nfa_transition_table = get_nfa_transition_table(inputs, states)

    converter = NfaToDfaConverter()
    converter.convert(inputs, states, nfa_transition_table, "subset_construction")


def get_nfa_transition_table(inputs, states):
    nfa_transition_table = [[None] * len(inputs) for i in range(len(states))]
 
    for i in range(len(inputs)):
        print("Enter the set of states that can be reached from state q following only arcs labeled", inputs[i])
        for j in range(len(states)):
            print(states[j], "-> ", end = "")
            output_states = input().split()
            nfa_transition_table[j][i] = output_states

    return nfa_transition_table


if __name__ == "__main__":
    main()
