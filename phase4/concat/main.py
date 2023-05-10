import json

def concatenate_nfa_machines(nfa1_file_path, nfa2_file_path):
    with open(nfa1_file_path) as f:
        nfa1 = json.load(f)
    with open(nfa2_file_path) as f:
        nfa2 = json.load(f)

    for key in nfa2:
        a = nfa2[key]
        if isinstance(a,str) and key != "initial_state":
            nfa2[key] = eval(nfa2[key])
    for key in nfa1:
        a = nfa1[key]
        if isinstance(a,str) and key != "initial_state":
            nfa1[key] = eval(nfa1[key])


    nfa2 = str(nfa2)
    nfa2 = nfa2.replace('"','')
    nfa2 = eval(nfa2)
    nfa1 = str(nfa1)
    nfa1 = nfa1.replace('"', '')
    nfa1 = eval(nfa1)


    number_of_nfa1_states = len(nfa1["states"])
    number_of_nfa2_states = len(nfa2["states"])
    nfa2 = str(nfa2)
    for i in range(number_of_nfa2_states):
        j = number_of_nfa1_states + i
        i = 'q' + str(i)
        j = '?' + str(j)
        nfa2 = nfa2.replace(i,j)
    nfa2 = nfa2.replace('?','q')
    nfa2 = eval(nfa2)

    final_state = 'q' + str(number_of_nfa2_states + number_of_nfa1_states)
    # Create a new NFA machine by concatenating the two machines
    new_nfa = {
        "states": nfa1["states"] | nfa2["states"] | {final_state},
        "input_symbols": nfa1["input_symbols"] | nfa2["input_symbols"],
        "transitions": {},
        "initial_state": nfa1["initial_state"],
        "final_states": {final_state}
    }

    # Copy the transitions from the first NFA machine
    for state, transitions in nfa1["transitions"].items():
        new_transitions = {}
        for symbol, next_states in transitions.items():
            new_transitions[symbol] = next_states
        new_nfa["transitions"][state] = new_transitions

    # Update the transitions from the second NFA machine
    for state, transitions in nfa2["transitions"].items():
        if state not in new_nfa["transitions"]:
            new_nfa["transitions"][state] = {}
        for symbol, next_states in transitions.items():
            if symbol not in new_nfa["transitions"][state]:
                new_nfa["transitions"][state][symbol] = set()
            new_nfa["transitions"][state][symbol] |= next_states

    for state in nfa1["final_states"]:
        new_nfa["transitions"][state][""] = {nfa2["initial_state"]}

    for state in nfa2["final_states"]:
        new_nfa["transitions"][state][""] = {final_state}

    return new_nfa

# Example usage
nfa1_file_path = "FA1.json"
nfa2_file_path = "FA2.json"
new_nfa = concatenate_nfa_machines(nfa1_file_path, nfa2_file_path)




for key in new_nfa:
    if not (isinstance(new_nfa[key],dict) or isinstance(new_nfa[key],str)):
        new_nfa[key] = str(new_nfa[key])

transitions = dict()
for key in new_nfa["transitions"]:
    a = new_nfa["transitions"][key]
    for key2 in new_nfa["transitions"][key]:
        new_nfa["transitions"][key][key2] = str(new_nfa["transitions"][key][key2])

new_nfa = str(new_nfa)

new_nfa = eval(new_nfa)
outfile = json.dumps(new_nfa,indent=4)

with open('concat_output.json','w') as f:
    f.write(outfile)

