import argparse
from solver.parser import parse_dimacs_cnf, convert_clauses_to_solver_format
from solver.algorithms.dpll import dpll
from solver.algorithms.resolution import resolution, dp

def solve(clauses, method="dpll", branching_method = None, verbose=False):
    if method == "dpll":
        return dpll(clauses, method=branching_method, verbose=verbose)
    if method == "dp":
        return dp(clauses, verbose=verbose)
    elif method == "resolution":
        return resolution(clauses, verbose=verbose)
    else:
        raise ValueError(f"Unknown method: {method}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run SAT solver with selected method.")
    parser.add_argument("file", type=str, help="Path to the CNF file to be solved.")
    parser.add_argument("--method", type=str, default="first", help="The method to solve the SAT problem. Options: resolution, dp, first, random, MAXO, MOMS, MAMS, JW, UP, GUP.")
    parser.add_argument("--verbose", action="store_true", help="Print detailed output during solving.")
    
    args = parser.parse_args()
    
    # Parse CNF file
    num_vars, num_clauses, clauses = parse_dimacs_cnf(args.file)
    clauses = convert_clauses_to_solver_format(clauses)
    
    # Solve using the chosen method
    result = solve(clauses, method=args.method, verbose=args.verbose)
    
    # Output the result
    if result:
        print("\nSATISFIABLE")
    else:
        print("\nUNSATISFIABLE")

if __name__ == "__main__":
    main()