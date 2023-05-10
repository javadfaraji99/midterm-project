import json

def star_nfa_machines(nfa_file_path):
    with open(nfa_file_path) as f:
        nfa = json.load(f)


    for key in nfa:
        a = nfa[key]
        if isinstance(a,str) and key != "initial_state":
            nfa[key] = eval(nfa[key])

    number_of_nfa_states = len(nfa["states"])

    nfa = str(nfa)
    nfa = nfa.replace('"','')

    nfa = eval(nfa)

    s = 'q' + str(number_of_nfa_states)
    s1 = 'q' + str(number_of_nfa_states + 1)

    # Create a new NFA machine by concatenating the two machines
    new_nfa = {
        "states": nfa["states"] | {s} | {s1},
        "input_symbols": nfa["input_symbols"],
        "transitions": nfa["transitions"],
        "initial_state": 'q0',
        "final_states": {s1}
    }

    # adding lambda transitions
    transition = {"" : {'q0',s1}}
    new_nfa["transitions"][s] = transition

    transition = {"": {s}}
    new_nfa["transitions"][s1] = transition

    for final_state in nfa["final_states"]:
        transition = {"": {s1}}
        new_nfa["transitions"][final_state].update(transition)


    return new_nfa

nfa_file_path = "FA.json"
new_nfa = star_nfa_machines(nfa_file_path)




for key in new_nfa:
    if not (isinstance(new_nfa[key],dict) or isinstance(new_nfa[key],str)):
        new_nfa[key] = str(new_nfa[key])

transitions = dict()
for key in new_nfa["transitions"]:
    a = new_nfa["transitions"][key]
    for key2 in new_nfa["transitions"][key]:
        new_nfa["transitions"][key][key2] = str(new_nfa["transitions"][key][key2])

print(new_nfa)
new_nfa = str(new_nfa)

new_nfa = eval(new_nfa)
outfile = json.dumps(new_nfa,indent=4)

with open('star_output.json','w') as f:
    f.write(outfile)

