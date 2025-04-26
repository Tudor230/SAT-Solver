
def unit_propagation(clauses, indentation="", verbose=True):
    """
    Apply unit propagation to simplify the clauses.
    """
    unit_clauses = [clause for clause in clauses if len(clause) == 1]
    counter = 0
    while unit_clauses:
        unit = unit_clauses.pop()
        literal = next(iter(unit))
        if verbose:
            print(f"{indentation}Found unit literal {literal}")
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                if verbose:
                    print(f"{indentation}Removed clause {set(clause)}")
                continue
            if -literal in clause:
                new_clause = clause - {-literal}
                counter += 1
                if len(new_clause) == 0:
                    if verbose:
                        print(f"{indentation}Removed {-literal} from clause {set(clause)} resulting in ∅")
                    return False, counter
                if verbose:
                    print(f"{indentation}Removed {-literal} from clause {set(clause)} resulting {set(new_clause)}")
                if len(new_clause) == 1:
                    unit_clauses.append(new_clause)
                new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)
        clauses = new_clauses
    return clauses, counter


def pure_literal_elimination(clauses, indentation="", verbose=True):
    """
    Apply pure literal elimination.
    """
    literals = set(l for clause in clauses for l in clause)
    pure_literals = {l for l in literals if -l not in literals}
    if not pure_literals:
        return clauses
    new_clauses = []
    for clause in clauses:
        if any(lit in pure_literals for lit in clause):
            if verbose:
                print(f"{indentation}Removed clause {set(clause)} because it contains a pure literal")
            continue
        new_clauses.append(clause)
    return pure_literal_elimination(new_clauses, indentation, verbose)