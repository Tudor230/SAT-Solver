from solver.utils import unit_propagation, pure_literal_elimination

def resolve(clause1, clause2):
    """
    Resolves two clauses and returns the resulting clause(s) if they can be resolved.
    """
    for literal in clause1:
        if -literal in clause2:
            new_clause = (clause1 - {literal}) | (clause2 - {-literal})
            return [new_clause]
    return []

def is_tautology(clause):
    """
    Check if a clause is a tautology (contains both a literal and its negation).
    """
    return any(-lit in clause for lit in clause)

def _resolution_core(clauses, dp=True, verbose=True):
    """
    Determines if the set of clauses is satisfiable using the resolution method.
    Logs each step in the process.
    """
    step = 1
    clauses = [frozenset(clause) for clause in clauses]

    # Print all initial clauses only if verbose is True
    if verbose:
        for clause in clauses:
            print(f"({step}) {set(clause)}")
            step += 1
        print()

    while True:
        new = set()

        # Check for an empty clause (unsatisfiable)
        if not clauses:
            if dp and verbose:
                print("Result: SATISFIABLE")
            return True

        # Apply Unit Propagation if requested
        if dp:
            clauses, counter = unit_propagation(clauses, verbose=verbose)
            if clauses is False:
                if dp and verbose:
                    print("Result: UNSATISFIABLE")
                return False
            if not clauses:
                if dp and verbose:
                    print("Result: SATISFIABLE")
                return True
            clauses = pure_literal_elimination(clauses, verbose=verbose)
            if not clauses:
                if dp and verbose:
                    print("Result: SATISFIABLE")
                return True

        clauses_set = set(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        diff = False

        for (c1, c2) in pairs:
            resolvents = resolve(c1, c2)
            for resolvent in resolvents:
                if not resolvent:
                    if verbose:
                        print(f"({step}) ∅ from {set(c1)} and {set(c2)}")
                        print("Result: UNSATISFIABLE")
                    return False
                if frozenset(resolvent) not in clauses_set and not is_tautology(resolvent):
                    if verbose:
                        print(f"({step}) {set(resolvent)} from {set(c1)} and {set(c2)}")
                    clauses_set.add(frozenset(resolvent))
                    new.add(frozenset(resolvent))
                    step += 1

        # If no new resolvents were added, it's SAT
        if not new:
            if verbose:
                print("\nNo new resolvent to be added")
                print("Result: SATISFIABLE")
            return True

        # Add new resolvents to clauses
        clauses.extend(new)

        # Apply unit propagation and pure literal elimination after each round
        if dp:
            # Apply unit propagation
            clauses, counter = unit_propagation(clauses, verbose=verbose)
            if clauses is False:
                if verbose:
                    print("Result: UNSATISFIABLE")
                return False
            if not clauses:
                if verbose:
                    print("Result: SATISFIABLE")
                return True

            # Apply pure literal elimination
            clauses = pure_literal_elimination(clauses, verbose=verbose)
            if not clauses:
                if verbose:
                    print("Result: SATISFIABLE")
                return True

# Public interface for resolution-only
def resolution(clauses, verbose=True):
    return _resolution_core(clauses, dp=False, verbose=verbose)

# Public interface for Davis–Putnam
def dp(clauses, verbose=True):
    return _resolution_core(clauses, dp=True, verbose=verbose)