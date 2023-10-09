from utils.automaton import Automaton

from convert.nfa_to_dfa import NfaToDfaConverter
from convert.enfa_to_nfa import ENfaToNfaConverter


def main():
    print("Select Operation:")
    print("1 - εNFA to NFA")
    print("2 - NFA to DFA")
    print("3 - εNFA to DFA")
    operation = input("Enter operation: ")

    if operation == 2:
        print("Select Method:")
        print("1 - Subset Construction")
        print("2 - Lazy")

        if method not in [1, 2]:
            print("Error: Invalid method")
            exit(1)

        method = input("Enter method: ")

    inputs = input("\nEnter input symbols (separated by white spaces): ").split()
    states = input("Enter states (separated by white spaces): ").split()
    start_state = input("Enter start state: ")
    final_states = input("Enter accepting state/s (separated by white spaces): ").split()
    nfa_transition_table = get_transition_table(inputs, states)

    automaton = Automaton(nfa_transition_table, inputs, states, start_state, final_states)    

    if (not validate(automaton)):
        print("Error: Invalid automaton")
        exit(1)

    if operation == "1":
        converter = ENfaToNfaConverter()
        converter.convert(automaton)
    if operation == "2":
        converter = NfaToDfaConverter()
        converter.convert(automaton, method = method)
    if operation == "3":
        pass
    
    exit(0)


def get_transition_table(inputs, states):
    transition_table = {state: {} for state in states}
 
    for i in inputs:
        print("Enter the set of states that can be reached from state q following only arcs labeled", i)
        for s in states:
            print(s, "-> ", end = "")
            output_states = input().split()
            transition_table[s][i] = output_states

    return transition_table

def validate(automaton):
    if automaton.start_state not in automaton.states:
        return False
    for state in automaton.final_states:
        if state not in automaton.states:
            return False
    for i in automaton.inputs:
        for state in automaton.transition_table[state][i]:
            if (state not in automaton.states):
                return False
    return True

if __name__ == "__main__":
    main()
