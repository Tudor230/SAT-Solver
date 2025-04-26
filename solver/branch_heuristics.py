import random
from collections import Counter
from solver.utils import *

def select_literal(clauses, indentation, verbose=True, method="first"):
    """
    Selects a branching literal according to the given method.
    """
    literals = [l for clause in clauses for l in clause]
    literal_set = set(literals)

    if method == "first":
        return next(iter(next(iter(clauses))))

    if method == "random":
        return random.choice(list(literal_set))

    if method == "MAXO":
        counter = Counter(literals)
        return counter.most_common(1)[0][0]

    if method == "MOMS":
        min_size = min(len(c) for c in clauses)
        min_clauses = [c for c in clauses if len(c) == min_size]
        counter = Counter(l for c in min_clauses for l in c)
        return counter.most_common(1)[0][0]

    if method == "MAMS":
        counter_all = Counter(literals)
        min_size = min(len(c) for c in clauses)
        min_clauses = [c for c in clauses if len(c) == min_size]
        counter_min = Counter(l for c in min_clauses for l in c)
        best_literal = None
        best_score = -1
        for l in literal_set:
            score = counter_all[l] + counter_min[-l]
            if score > best_score:
                best_score = score
                best_literal = l
        return best_literal

    if method == "JW":
        scores = {}
        for clause in clauses:
            for l in clause:
                scores[l] = scores.get(l, 0) + 2 ** (-len(clause))
        return max(scores, key=scores.get)

    if method == "UP" or method == "GUP":
        best_literal = None
        best_score = -1
        for l in literal_set:
            # Try setting l = True
            score = count_unit_propagations(clauses, l, indentation, verbose)
            if method == "GUP" and (score == 0 or score == float('inf')):
                return l  # Immediate contradiction OR immediate satisfaction
            if score > best_score:
                best_score = score
                best_literal = l
        return best_literal

    if method == "SUP":
        candidates = []
        for m in ["MAXO", "MOMS", "MAMS", "JW"]:
            candidates.append(select_literal(clauses, indentation, method=m))
        candidates = list(set(candidates))  # Remove duplicates
        best_literal = None
        best_score = -1
        for l in candidates:
            score = count_unit_propagations(clauses, l, indentation, verbose)
            if score > best_score:
                best_score = score
                best_literal = l
        return best_literal

    raise ValueError(f"Unknown selection method: {method}")


def count_unit_propagations(clauses, literal, indentation, verbose):
    """
    Try assigning 'literal = True' and count how many unit propagations happen.
    If conflict occurs, return -1.
    """
    new_clauses = clauses + [frozenset([literal])]
    result, count = unit_propagation(new_clauses, indentation, verbose = False)
    if result is False:
        return 0  # conflict
    if not result:
        return float("inf")
    return count