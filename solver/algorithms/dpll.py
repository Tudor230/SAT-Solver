from solver.utils import unit_propagation, pure_literal_elimination
from solver.branch_heuristics import select_literal

def dpll(clauses, branch=None, indent=0, verbose=True, method="first", splits = 0):
    """
    DPLL algorithm for SAT solving.
    Accepts clauses in DIMACS-style format (list of sets of integers).
    """
    indentation = "  " * indent
    # 1. Unit Propagation
    clauses, counter = unit_propagation(clauses, indentation, verbose)
    if clauses is False:
        if verbose:
            msg = f"{indentation}Unsatisfiable after unit propagation"
            if branch is not None:
                msg += f" for branch {branch}"
            print(msg)
        if indent == 0 and verbose:
            print("Result: UNSATISFIABLE")
        return False, splits
    elif not clauses:
        if verbose:
            msg = f"{indentation}Satisfiable after unit propagation"
            if branch is not None:
                msg += f" for branch {branch}"
            print(msg)
        if indent == 0 and verbose:
            print("Result: SATISFIABLE")
        return True, splits

    # 2. Pure Literal Elimination
    clauses = pure_literal_elimination(clauses, indentation, verbose)
    if not clauses:
        if verbose:
            msg = f"{indentation}Satisfiable after pure literal elimination"
            if branch is not None:
                msg += f" for branch {branch}"
            print(msg)
        if indent == 0 and verbose:
            print("Result: SATISFIABLE")
        return True, splits

    # 3. Choose a branching literal
    literal = select_literal(clauses, indentation, verbose, method=method)
    if literal is None:
        # No literal selected, backtrack
        if verbose:
            print(f"{indentation}No literal could be selected, backtracking")
        return False, splits
    splits += 1

    # 4. Try literal = True
    if verbose:
        print(f"\n{indentation}Branching on {literal} = True")
    new_clauses_true = clauses + [frozenset([literal])]
    result, splits = dpll(new_clauses_true, literal, indent + 1, verbose, method, splits)
    if result:
        if verbose:
            print(f"{indentation}Satisfiable with {literal} = True")
        if indent == 0 and verbose:
            print("Result: SATISFIABLE")
        return True, splits

    # 5. Try literal = False
    if verbose:
        print(f"\n{indentation}Branching on {literal} = False")
    new_clauses_false = clauses + [frozenset([-literal])]
    result, splits = dpll(new_clauses_false, -literal, indent + 1, verbose, method, splits)
    if result:
        if verbose:
            print(f"{indentation}Satisfiable with {literal} = False")
        if indent == 0 and verbose:
            print("Result: SATISFIABLE")
        return True, splits

    # 6. Neither branch led to satisfiability
    if verbose:
        print(f"{indentation}Unsatisfiable: both branches failed for literal {literal}")
    if indent == 0 and verbose:
        print("Result: UNSATISFIABLE")
    return False, splits