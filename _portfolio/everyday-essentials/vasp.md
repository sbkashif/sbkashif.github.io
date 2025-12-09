---
layout: portfolio_item
title: "Vasp"
permalink: /everyday-essentials/vasp/
date_created: 2025-11-02
last_modified: 2025-11-02
hidden: true
---

# vasp parallelization
vasp uses two main parallelization types to distribute the computational load across CPUs.

**mpi (message passing interface)**

*concept*: allows independent processes (ranks) to communicate by sending messages, typically across different cores and nodes.

*vasp role*: the primary scaling method. Each MPI process handles a fraction of the total workload (e.g., k-points or bands).
Control Point: the core count specified in the job script (mpirun -n N or #SBATCH --ntasks=N).

**shared memory parallelization (ncore)**

*concept*: allows multiple computational threads within a single MPI process to share memory.

*vasp role*: Used to accelerate memory-intensive operations (FFTs, diagonalization).
Control Point: the NCORE tag in the INCAR file.

### resource definitions
Core ($\mathbf{N_{\text{cores}}}$): the total number of CPU threads allocated to your job (the 'N' in mpirun -n N).
Node ($\mathbf{N_{\text{nodes}}}$): A physical server containing multiple cores. Your request, --nodes=1, means all processes run on the same server.

## 💻 Hardware Request Settings (SLURM/PBS)

the key is requesting a core count that is highly divisible.
### the Core Count Rule
Choose a number of cores that is a highly composite number to allow for flexible and efficient parallel grouping (NCORE and KPAR). When number of cores are 32, divisors: 2, 4, 8, 16 are best for vasp parallelization.

### Slurm settings

`#SBATCH --ntasks-per-node=32`

### MPI Execution (must match the request)
`$MPIRUN -n 32 $VASP_DIR/bin/vasp_std &> vasp.out`


## ⚙️ vasp Parallelization Settings (INCAR Tags)
These tags define how the total allocated cores are internally divided.

### $\mathbf{NCORE}$ (the Primary Parallelization Flag)
Purpose: Controls the number of cores that work together in a single shared-memory group.
Principle: When vasp runs with $N_{\text{cores}}$, $NCORE$ divides the job into groups:
$$\text{Number of Groups} = \frac{N_{\text{cores}}}{NCORE}$$

Expert Recommendation: Set $\mathbf{NCORE}$ to a divisor of $N_{\text{cores}}$ that is close to $\mathbf{\sqrt{N_{\text{cores}}}}$.

For 32 cores: $\sqrt{32} \approx 5.66$.
Optimal NCORE: 4 or 8. Start with 8.

Note: Use $\mathbf{NCORE=1}$ only for very small systems where communication overhead is high.

### $\mathbf{KPAR}$ (K-Point Parallelization)
Purpose: Divides the k-point list among core groups. Each group calculates a subset of k-points independently.
Constraint: $\mathbf{KPAR}$ must evenly divide both the total cores ($\mathbf{N_{\text{cores}}}$) and the k-points ($\mathbf{N_{\text{kpoints}}}$).
Recommendation:
Start with $\mathbf{KPAR=1}$ (default).
Only increase $\mathbf{KPAR}$ if $\mathbf{N_{\text{kpoints}}}$ is high (e.g., > 100).

### $\mathbf{LPLANE}$ (Memory Parallelization)
Purpose: Controls the distribution of the plane-wave basis set across the cores, reducing the memory load on individual processes.
Recommendation: Set LPLANE = .TRUE.. This is highly recommended for large-scale calculations or systems with high ENCUT values.

## 📈 Performance Verification (OUTCAR Analysis)

Check the end of the vasp OUTCAR file after a short test run.

Check Settings: vasp prints the final parallelization setup:

NCORE = 8
KPAR = 1


## Verify these match your INCAR inputs.

Analyze Timing: Look for the General and Subroutines timing table.
Goal: the time for the self-consistency cycle (e.g., RMM-DIIS or ZGEMM) should be minimized.

Warning Sign: If MPI Communication time is large, your $\mathbf{NCORE}$ might be too high, indicating communication overhead is dominating computation.