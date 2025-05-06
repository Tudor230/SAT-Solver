import os
import time
import argparse
import gc
from solver.solver import solve
from solver.parser import parse_dimacs_cnf, convert_clauses_to_solver_format


def solve_cnf_file(file_path, method="first", verbose=False):
    """Solve a single CNF file and measure time and memory."""
    num_vars, num_clauses, clauses = parse_dimacs_cnf(file_path)
    solver_clauses = convert_clauses_to_solver_format(clauses)

    start_time = time.perf_counter()
    splits = [0]
    result = [False]
    def run_solver():
        if method == "resolution":
            result[0] = solve(solver_clauses, method, verbose=verbose)
        elif method == "dp":
            result[0] = solve(solver_clauses, method, verbose=verbose)
        else:
            result[0], splits[0] = solve(solver_clauses, branching_method=method, verbose=verbose)
        return

    run_solver()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return elapsed_time, splits[0], result[0]

def test_folder(folder_path, method="first"):
    times = []
    splits_data = []
    satisfiable = True
    failed_files = []

    files = sorted(f for f in os.listdir(folder_path) if f.endswith(".cnf"))

    for file_name in files:
        print(f"Testing {file_name} with method {method}")
        file_path = os.path.join(folder_path, file_name)
        elapsed_time, splits, result = solve_cnf_file(file_path, method=method)
        times.append(elapsed_time)
        splits_data.append(splits)

        if not result:
            satisfiable = False
            failed_files.append(file_name)

    gc.collect()

    avg_time = sum(times) / len(times) if times else 0
    avg_splits = sum(splits_data) / len(splits_data) if splits_data else 0
    return satisfiable, avg_time, avg_splits, failed_files

def benchmark_methods(folder_path, methods):
    results = {}
    for method in methods:
        print(f"\nTesting method: {method}")
        satisfiable, avg_time, avg_splits, failed_files = test_folder(folder_path, method=method)
        print(f"Status: {"OK" if satisfiable else "FAILED"}")
        print(f"Average time for {method}: {avg_time:.4f} seconds")
        print(f"Average splits for {method}: {avg_splits}")
        if failed_files:
            print(f"Files failed for {method}: {failed_files}")
        results[method] = {
            "time": avg_time,
            "splits": avg_splits,
            "failed_files": failed_files
        }
    return results


def save_results_to_file(results, folder_path, filename="benchmark_results.txt"):
    """Save benchmark results to a text file."""
    folder_name = os.path.basename(os.path.normpath(folder_path))
    full_path = os.path.join(folder_name + "_" + filename)
    with open(full_path, "w") as f:
        f.write(f"Benchmark Results for folder: {folder_path}\n\n")
        for method, data in results.items():
            f.write(f"Method: {method}\n")
            f.write(f"  Average Time: {data['time']:.4f} seconds\n")
            f.write(f"  Average Splits: {data['splits']}\n")
            if data['failed_files']:
                f.write(f"  Failed Files: {', '.join(data['failed_files'])}\n")
            else:
                f.write("  Failed Files: None\n")
            f.write("\n")
    print(f"Saved benchmark results to {full_path}")

# Main function to run the benchmark
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark DPLL solver with memory profiling.")
    parser.add_argument("--folder", type=str, default="tests/uf20-91", help="Folder containing CNF files.")
    parser.add_argument("--methods", type=str, nargs="+", default=["first", "MAXO", "MOMS", "MAMS", "JW", "GUP", "SUP"], help="List of methods to test.")
    args = parser.parse_args()

    # Run benchmark
    results = benchmark_methods(args.folder, methods=args.methods)

    save_results_to_file(results, args.folder)