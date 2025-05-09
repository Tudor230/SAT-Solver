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
