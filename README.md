# SAT-Solver

A modular SAT solver implemented in Python, supporting multiple solving algorithms and branching heuristics.

## Features

* **Multiple Solving Algorithms**:

  * Davis–Putnam–Logemann–Loveland (DPLL) algorithm
  * Davis–Putnam (DP) procedure
  * Resolution-based solving

* **Branching Heuristics for DPLL**:

  * First
  * Random
  * Maximum Occurrences in clauses of Minimum Size (MOMS)
  * Maximum Occurrences (MAXO)
  * Maximum Occurrences in clauses of Average Size (MAMS)
  * Jeroslow-Wang (JW)
  * Unit Propagation (UP)
  * Generalized Unit Propagation (GUP)
  * Selective Unit Propagation (SUP)

* **Verbose Mode**: Provides detailed output during the solving process.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Tudor230/SAT-Solver.git
   cd SAT-Solver
   ```



2. **Run the Solver**:

   Ensure you have Python 3 installed. Use the command-line interface to run the solver with a CNF file:

   ```bash
   python -m solver.solver path_to_cnf_file.cnf --method first --verbose
   ```



## Input Format

The solver accepts CNF files in the standard DIMACS format. Each file should begin with a problem line (e.g., `p cnf 3 2`) followed by one clause per line, ending with `0`.

## Usage Options

* **`--method`**: Specify the solving method. Options include:

  * `dp`: Davis–Putnam procedure with resolution and simplification.
  * `resolution`: Pure resolution-based solving.
  * `first`, `random`, `MAXO`, `MOMS`, `MAMS`, `JW`, `UP`, `GUP`, `SUP`: Heuristics for DPLL branching.

* **`--verbose`**: Enable detailed output during solving.

## Output

After solving, the program outputs:

* `SATISFIABLE` if a satisfying assignment exists.
* `UNSATISFIABLE` if no such assignment exists.

## Repository Structure

* **`solver/`**:

  * **`parser.py`**: Parses DIMACS-formatted CNF files into internal data structures.
  * **`solver.py`**: Main interface for solving SAT problems; handles command-line arguments and invokes the appropriate solving algorithm.
  * **`algorithms/`**:

    * **`dpll.py`**: Implements the DPLL algorithm.
    * **`resolution.py`**: Implements the resolution-based algorithm and the Davis-Putnam (DP) procedure.
  * **`heuristics.py`**: Provides various branching heuristics used by the DPLL algorithm.

* **`tests/`**: Contains tests to verify the correctness of the parser and solver components.

## License

This project is licensed under the MIT License.


