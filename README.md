---

# SAT-Solver

A **modular and extensible SAT solver** implemented in Python, supporting multiple solving algorithms and advanced branching heuristics. Designed for educational purposes, experimentation, and research on SAT-solving techniques.

---

## ✨ Features

* **Multiple Solving Algorithms**

  * **DPLL** (Davis–Putnam–Logemann–Loveland)
  * **DP** (Davis–Putnam)
  * **Resolution-based solving**

* **Branching Heuristics for DPLL**

  * `first`
  * `random`
  * `MAXO`: Maximum Occurrences
  * `MOMS`: Maximum Occurrences in clauses of Minimum Size
  * `MAMS`: Combination of MAXO and MOMS
  * `JW`: Jeroslow-Wang
  * `UP`: Unit Propagation
  * `GUP`: Greedy Unit Propagation
  * `SUP`: Selective Unit Propagation

* **Verbose Mode**: Step-by-step tracing of the solving process.

* **Modular Architecture**: Easy to extend with new algorithms and heuristics.

* **Testing Suite**: Ensures correctness of parsing and solving logic.

---

## 📦 Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Tudor230/SAT-Solver.git
   cd SAT-Solver
   ```

2. **(Optional) Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   This project uses only the Python standard library. No extra dependencies are required.

---

## 🚀 Usage

```bash
python -m solver.solver path_to_cnf_file.cnf --method METHOD_NAME [--verbose]
```

### Options:

| Argument               | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `path_to_cnf_file.cnf` | Input CNF file in DIMACS format                   |
| `--method`             | Solving method or branching heuristic (see below) |
| `--verbose`            | (Optional) Print step-by-step solving process     |

### Available Methods:

* **Solvers**:

  * `dp`: Davis–Putnam procedure
  * `resolution`: Resolution-based algorithm

* **DPLL Heuristics**:

  * `first`, `random`, `MAXO`, `MOMS`, `MAMS`, `JW`, `UP`, `GUP`, `SUP`

---

## 📄 CNF Input Format

The input file must follow the [DIMACS CNF format](https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps):

```
c This is a comment
p cnf 3 2
1 -3 0
2 3 -1 0
```

* `p cnf <num_variables> <num_clauses>` — declares the number of variables and clauses.
* Each clause is a line of literals ending with `0`.

---

## ✅ Output

The solver prints:

* `SATISFIABLE` — If a satisfying assignment is found.
* `UNSATISFIABLE` — If the formula is unsatisfiable.

With `--verbose`, it will also print:

* Branching decisions
* Clause simplifications
* Unit propagations

---

## 📁 Project Structure

```
SAT-Solver/
├── solver/
│   ├── parser.py         # DIMACS parser
│   ├── solver.py         # CLI + solving orchestration
│   ├── heuristics.py     # Heuristic functions for DPLL
│   └── algorithms/
│       ├── dpll.py       # DPLL implementation
│       └── resolution.py # DP and resolution algorithms
├── tests/                # Unit tests
└── README.md
```

## 🧪 Running Tests

The `SAT-Solver` project includes a test suite to verify the correctness of its components, such as the CNF parser, solving algorithms, and heuristics.

### Running Tests

To execute the tests, use the following command:

```bash
python -m tests.test --folder FOLDER_PATH --methods METHODS
```

Replace `FOLDER_PATH` with the path to the directory containing your CNF files, and `METHODS` with the solving methods or heuristics you wish to test. For example:

```bash
python -m tests.test --folder examples/ --methods dp dpll
```

This command will run the tests on all CNF files in the `examples/` directory using the `dp` and `dpll` methods.

### Saving Test Results

After running the tests, the results will be saved as a text file in the root directory of the project.

This file contains detailed information about each test case, including the input folder, the method used, and the average time and splits (for DPLL).

---

## 🙋‍♀️ Contributing

Contributions are welcome! To add a new heuristic or algorithm:

1. Fork the repository.
2. Add your logic under `solver/algorithms/` or `solver/heuristics.py`.
3. Write unit tests in the `tests/` directory.
4. Submit a pull request with a clear description.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

This project was built for educational and research purposes. It draws on foundational techniques from SAT solving literature and standard algorithm implementations.

---
