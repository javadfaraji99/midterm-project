
#!/usr/bin/env python3
"""Classes and methods for working with deterministic finite automata."""

from collections import deque
from itertools import chain
from automata.base.utils import PartitionRefinement


class DFA():
    """A deterministic finite automaton."""

    __slots__ = ('states', 'input_symbols', 'transitions',
                 'initial_state', 'final_states')

    def __init__(self, states, input_symbols, transitions,
                 initial_state, final_states):
        """Initialize a complete DFA."""
        self.states = states
        self.input_symbols = input_symbols
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def _compute_reachable_states(self):
        """Compute the states which are reachable from the initial state."""
        visited_set = set()
        queue = deque()

        queue.append(self.initial_state)
        visited_set.add(self.initial_state)

        while queue:
            state = queue.popleft()

            for next_state in self.transitions[state].values():
                if next_state not in visited_set:
                    visited_set.add(next_state)
                    queue.append(next_state)

        return visited_set

    def minify(self, retain_names=False):
        """
        Create a minimal DFA which accepts the same inputs as this DFA.

        First, non-reachable states are removed.
        Then, similiar states are merged using Hopcroft's Algorithm.
            retain_names: If True, merged states retain names.
                          If False, new states will be named 0, ..., n-1.
        """

        # Compute reachable states and final states
        reachable_states = self._compute_reachable_states()
        reachable_final_states = self.final_states & reachable_states

        return self._minify(
            reachable_states=reachable_states,
            input_symbols=self.input_symbols,
            transitions=self.transitions,
            initial_state=self.initial_state,
            reachable_final_states=reachable_final_states,
            retain_names=retain_names)

    @classmethod
    def _minify(cls, *, reachable_states, input_symbols, transitions, initial_state,
                reachable_final_states, retain_names):
        """Minify helper function. DFA data passed in must have no unreachable states."""

        # First, assemble backmap and equivalence class data structure
        eq_classes = PartitionRefinement(reachable_states)
        refinement = eq_classes.refine(reachable_final_states)

        final_states_id = refinement[0][0] if refinement else next(iter(eq_classes.get_set_ids()))

        transition_back_map = {
            symbol: {
                end_state: list()
                for end_state in reachable_states
            }
            for symbol in input_symbols
        }

        for start_state, path in transitions.items():
            if start_state in reachable_states:
                for symbol, end_state in path.items():
                    transition_back_map[symbol][end_state].append(start_state)

        origin_dicts = tuple(transition_back_map.values())
        processing = {final_states_id}

        while processing:
            # Save a copy of the set, since it could get modified while executing
            active_state = tuple(eq_classes.get_set_by_id(processing.pop()))
            for origin_dict in origin_dicts:
                states_that_move_into_active_state = chain.from_iterable(
                    origin_dict[end_state] for end_state in active_state
                )

                # Refine set partition by states moving into current active one
                new_eq_class_pairs = eq_classes.refine(states_that_move_into_active_state)

                for (YintX_id, YdiffX_id) in new_eq_class_pairs:
                    # Only adding one id to processing, since the other is already there
                    if YdiffX_id in processing:
                        processing.add(YintX_id)
                    else:
                        if len(eq_classes.get_set_by_id(YintX_id)) <= len(eq_classes.get_set_by_id(YdiffX_id)):
                            processing.add(YintX_id)
                        else:
                            processing.add(YdiffX_id)

        eq_class_name_pairs = []
        a = list(eq_classes.get_sets())
        for se in a:
            s = list(se)
            s.sort()
            s = ''.join(s)
            eq_class_name_pairs.append((s,se))
        # need a backmap to prevent constant calls to index
        back_map = {
            state: name
            for name, eq in eq_class_name_pairs
            for state in eq
        }

        new_input_symbols = str(input_symbols)

        new_states = set()
        for state in back_map.values():
            new_states.add(state)
        new_states = str(new_states)

        new_initial_state = str(back_map[initial_state])

        new_final_states = set()
        for acc in reachable_final_states:
            new_final_states.add(back_map[acc])
        new_final_states = str(new_final_states)

        new_transitions = {
            name: {
                letter: back_map[transitions[next(iter(eq))][letter]]
                for letter in input_symbols
            }
            for name, eq in eq_class_name_pairs
        }

        return cls(
            states=new_states,
            input_symbols=new_input_symbols,
            transitions=new_transitions,
            initial_state=new_initial_state,
            final_states=new_final_states,
        )

import json



with open('input1.json', 'r') as f:
    dfa = json.load(f)

dfa = str(dfa)

dfa = dfa.replace('"','')

dfa = eval(dfa)

dfa = DFA( dfa['states'] , dfa['input_symbols'] , dfa['transitions'] , dfa['initial_state'] , dfa['final_states'] )
new_dfa = dfa.minify()



minimized_dfa = dict()
minimized_dfa['states'] = new_dfa.states
minimized_dfa['input_symbols'] = new_dfa.input_symbols
minimized_dfa['transitions'] = new_dfa.transitions
minimized_dfa['initial_state'] = new_dfa.initial_state
minimized_dfa['final_states'] = new_dfa.final_states



json_file = json.dumps(minimized_dfa,indent=4)
with open("output1.json",'w') as f:
    f.write(json_file)

