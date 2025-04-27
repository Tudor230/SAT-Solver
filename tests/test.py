import os
import time
import argparse
import gc
import numpy as np
import matplotlib.pyplot as plt
from memory_profiler import memory_usage
from matplotlib.ticker import ScalarFormatter, LogLocator, LogFormatter
from solver.solver import *


# def get_memory_usage():
#     """Get the current memory usage in KB."""
#     process = psutil.Process(os.getpid())
#     memory_info = process.memory_info()
#     memory_kb = memory_info.rss / 1024  # Convert from bytes to KB
#     return memory_kb


def solve_cnf_file(file_path, method="first", verbose=False):
    """Solve a single CNF file and measure time and memory."""
    num_vars, num_clauses, clauses = parse_dimacs_cnf(file_path)
    solver_clauses = convert_clauses_to_solver_format(clauses)

    # Measure memory before solving
    start_time = time.perf_counter()
    splits = [0]
    result = [False]
    # Track memory usage over time using memory_usage
    def run_solver():
        """Run the solver function inside a memory tracking context."""
        if method == "resolution":
            result[0] = resolution(solver_clauses, dp=False, verbose=verbose)
        elif method == "dp":
            result[0] = resolution(solver_clauses, dp=True, verbose=verbose)
        else:
            result[0], splits[0] = dpll(solver_clauses, method=method, verbose=verbose)
        return

    # Track memory usage during the solving process
    memory_usage_list = memory_usage(run_solver)  # Memory usage over time while running solver

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    # Calculate average memory usage during the solving process
    avg_memory_usage = sum(memory_usage_list) / len(memory_usage_list) if memory_usage_list else 0
    return elapsed_time, avg_memory_usage, splits[0], result[0]

def test_folder(folder_path, method="first"):
    times = []
    memory_usages = []
    splits_data = []
    memory_data = []
    satisfiable = True
    failed_files = []

    files = sorted(f for f in os.listdir(folder_path) if f.endswith(".cnf"))

    for file_name in files:
        print(f"Testing {file_name} with method {method}")
        file_path = os.path.join(folder_path, file_name)
        elapsed_time, avg_memory_usage, splits, result = solve_cnf_file(file_path, method=method)
        times.append(elapsed_time)
        memory_usages.append(avg_memory_usage)
        splits_data.append(splits)
        # Capture memory data for plotting (time, average memory)
        memory_data.append((elapsed_time, avg_memory_usage))

        if not result:
            satisfiable = False
            failed_files.append(file_name)  # <<< Add file name to list if it failed

    gc.collect()
    time.sleep(0.1)

    # Plot results
    # plot_memory_usage(memory_data)

    avg_time = sum(times) / len(times) if times else 0
    avg_memory = sum(memory_usages) / len(memory_usages) if memory_usages else 0
    avg_splits = sum(splits_data) / len(splits_data) if splits_data else 0
    return satisfiable, avg_time, avg_memory, avg_splits, failed_files

def plot_memory_usage(memory_data):
    """Plot average memory usage over time."""
    times = [data[0] for data in memory_data]
    memory = [data[1] for data in memory_data]

    plt.figure(figsize=(10, 6))
    plt.plot(times, memory, label="Average Memory Usage (KB)", color="green", marker="o")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Average Memory Usage (KB)")
    plt.title("Average Memory Usage Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"average_memory_usage_plot.png")
    print("Saved average memory usage plot to average_memory_usage_plot.png")

def benchmark_methods(folder_path, methods):
    results = {}
    for method in methods:
        print(f"\nTesting method: {method}")
        satisfiable, avg_time, avg_memory, avg_splits, failed_files = test_folder(folder_path, method=method)
        print(f"Status: {"OK" if satisfiable else "FAILED"}")
        print(f"Average time for {method}: {avg_time:.4f} seconds")
        print(f"Average memory usage for {method}: {avg_memory:.2f} KB")
        print(f"Average splits for {method}: {avg_splits}")
        if failed_files:
            print(f"Files failed for {method}: {failed_files}")
        results[method] = {
            "time": avg_time,
            "memory": avg_memory,
            "splits": avg_splits,
            "failed_files": failed_files  # <<< save the list here too if you want
        }
    return results

def plot_results(results, folder_path):
    methods = list(results.keys())
    times = [results[method]["time"] for method in methods]
    memory = [results[method]["memory"] for method in methods]
    splits = [results[method]["splits"] for method in methods]
    folder_name = os.path.basename(os.path.normpath(folder_path))

    # --- Plot 1: Time ---
    plt.figure(figsize=(8, 5))
    plt.bar(methods, times, color="skyblue")
    plt.xlabel("Branching Method")
    plt.ylabel("Average Solving Time (seconds)")
    plt.title("Average Solving Time per Branching Method")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.yscale('log')
    plt.gca()
    plt.tight_layout()
    plt.savefig(f"{folder_name}_benchmark_time.png")
    print("Saved time plot to benchmark_time.png")

    # --- Plot 2: Memory ---
    plt.figure(figsize=(8, 5))
    plt.bar(methods, memory, color="lightgreen")
    plt.xlabel("Branching Method")
    plt.ylabel(f"Average Memory Usage (KB)")
    plt.title("Average Memory Usage per Branching Method")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(f"{folder_name}_benchmark_memory.png")
    print("Saved memory plot to benchmark_memory.png")

    # --- Plot 3: Splits ---
    plt.figure(figsize=(8, 5))
    plt.bar(methods, splits, color="salmon")
    plt.xlabel("Branching Method")
    plt.ylabel("Average Number of Splits")
    plt.title("Average Splits per Branching Method")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.yscale('log')
    ax = plt.gca()
    ax.yaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_minor_locator(plt.NullLocator())
    yticks = sorted(set([round(s, -int(np.floor(np.log10(s)))) for s in splits]))
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{int(t):,}" for t in yticks])
    ax.grid(False)
    for y in yticks:
        ax.axhline(y, color='gray', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(f"{folder_name}_benchmark_splits.png")
    print("Saved splits plot to benchmark_splits.png")


def save_results_to_file(results, folder_path, filename="benchmark_results.txt"):
    """Save benchmark results to a text file."""
    folder_name = os.path.basename(os.path.normpath(folder_path))
    full_path = os.path.join(folder_name + "_" + filename)
    with open(full_path, "w") as f:
        f.write(f"Benchmark Results for folder: {folder_path}\n\n")
        for method, data in results.items():
            f.write(f"Method: {method}\n")
            f.write(f"  Average Time: {data['time']:.4f} seconds\n")
            f.write(f"  Average Memory Usage: {data['memory']:.2f} KB\n")
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

    # plot_results(results, args.folder)
    save_results_to_file(results, args.folder)