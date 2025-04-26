import cProfile
from solver.branch_heuristics import select_literal
from solver.utils import *

def resolve(clause1, clause2):
    """
    Resolves two clauses and returns the resulting clause(s) if they can be resolved.
    """
    for literal in clause1:
        if -literal in clause2:
            new_clause = (clause1 - {literal}) | (clause2 - {-literal})
            return [new_clause]
    return []



def resolution(clauses, dp=True, verbose=True):
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
                if new and dp:
                    new_clauses = clauses + list(new)
                    unit_clauses, counter = unit_propagation(new_clauses, verbose=verbose)
                    if unit_clauses is False:
                        if verbose:
                            print("Result: UNSATISFIABLE")
                        return False
                    if not unit_clauses:
                        if verbose:
                            print("Result: SATISFIABLE")
                        return True
                    pure_clauses = pure_literal_elimination(unit_clauses, verbose=verbose)
                    if not pure_clauses:
                        if verbose:
                            print("Result: SATISFIABLE")
                        return True
                    if new_clauses != pure_clauses:
                        clauses = list(map(frozenset, pure_clauses))
                        diff = True
                        break
            if diff:
                break
        if not new:
            if verbose:
                print("\nNo new resolvent to be added")
                print("Result: SATISFIABLE")
            return True
        if not diff:
            clauses.extend(new)


def is_tautology(clause):
    """
    Check if a clause is a tautology (contains both a literal and its negation).
    """
    return any(-lit in clause for lit in clause)


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


def parse_dimacs_cnf(file_path):
    """
    Parse a DIMACS CNF file to extract the problem variables and clauses.

    Args:
    - file_path (str): The path to the DIMACS CNF file.

    Returns:
    - num_vars (int): Number of variables in the CNF formula.
    - num_clauses (int): Number of clauses in the CNF formula.
    - clauses (list of sets): A list of sets, each containing the literals in the corresponding clause.
    """
    num_vars = 0
    num_clauses = 0
    clauses = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip comments (lines starting with 'c')
            if line.startswith('c') or line.startswith('%') or line.startswith('0'):
                continue

            # Problem line starts with 'p', e.g., 'p cnf 20 91'
            if line.startswith('p'):
                _, _, num_vars, num_clauses = line.split()
                num_vars = int(num_vars)
                num_clauses = int(num_clauses)
                continue

            # Process clauses (lines containing integers, e.g., '13 15 -5 0')
            try:
                clause = set(map(int, line.split()))  # Convert to integers and store as a set
                # Ensure the clause ends with 0, which is the delimiter in DIMACS format
                if 0 in clause:
                    clause.remove(0)  # Remove the trailing 0
                    clauses.append(clause)
            except ValueError:
                print(f"Warning: Invalid clause line format in file: {line}")
    return num_vars, num_clauses, clauses


def convert_clauses_to_solver_format(clauses):
    """
    Convert DIMACS clauses (list of sets of integers) to the format used by your solver.
    The format is a list of sets, where each set represents a clause.

    Args:
    - clauses (list of sets): The clauses parsed from a DIMACS CNF file.

    Returns:
    - solver_clauses (list of sets): A list of sets representing the clauses in the format used by the solver.
    """
    solver_clauses = []

    for clause in clauses:
        # Convert each clause into the format used by your solver (no changes needed in this case)
        solver_clauses.append(clause)

    return solver_clauses


def print_clauses(clauses):
    """
    Print the clauses in a readable format.

    Args:
    - clauses (list of sets): A list of sets, each containing the literals in the corresponding clause.
    """
    for clause in clauses:
        print(f"({' ∨ '.join(str(lit) for lit in clause)})")


# file_path = "tests/uf20-91/uf20-0312.cnf"
#
# num_vars, num_clauses, clauses = parse_dimacs_cnf(file_path)
# solver_clauses = convert_clauses_to_solver_format(clauses)
# print(f"Number of variables: {num_vars}")
# print(f"Number of clauses: {num_clauses}")
#
# profiler = cProfile.Profile()
# profiler.enable()
#
# result, splits = dpll([frozenset(clause) for clause in solver_clauses], verbose=True, method="SUP")
# print(splits)
# # resolution([frozenset(clause) for clause in solver_clauses], verbose=True, dp=True)
#
# profiler.disable()
# profiler.dump_stats("profile_output.prof")

