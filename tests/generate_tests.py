import random
import os
def generate_3sat_cnf(num_vars, num_clauses, seed=None):
    if seed is not None:
        random.seed(seed)
    
    clauses = []
    
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, num_vars)
            lit = var if random.choice([True, False]) else -var
            clause.add(lit)
        clauses.append(list(clause))
    
    return clauses


def write_dimacs_file(filename, num_vars, clauses):
    with open(filename, 'w') as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

            
def generate_multiple_files(folder, num_files=100, num_vars=6, num_clauses=30):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Generate 100 files with fixed num_vars=6 and num_clauses=30
    for i in range(num_files):
        # Generate clauses with 6 variables and 30 clauses
        clauses = generate_3sat_cnf(num_vars, num_clauses, seed=i)
        
        # Define the filename with an index to ensure uniqueness
        filename = os.path.join(folder, f"cnf_{num_vars}v_{num_clauses}c_{i+1}.cnf")
        
        # Write the CNF to the file
        write_dimacs_file(filename, num_vars, clauses)
        print(f"Written: {filename}")

# Folder to save the CNF files
folder = "cnf/generated"

# Generate and write 100 CNF files with 6 variables and 30 clauses
generate_multiple_files(folder, num_files=100, num_vars=6, num_clauses=30)

# # Generate and write CNF files
# sizes = [(6,20),(6,30),(8,20),(8,30),(10,50),(20, 80), (30, 120), (40, 160)]


# for idx, (num_vars, num_clauses) in enumerate(sizes, 1):
#     clauses = generate_3sat_cnf(num_vars, num_clauses, seed=idx)
#     filename = f"cnf_{num_vars}v_{num_clauses}c.cnf"
#     write_dimacs_file(filename, num_vars, clauses)
#     print(f"Written: {filename}")
