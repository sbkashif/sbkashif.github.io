---
layout: post
title: 'Parallelizing a molecular dynamics code using MPI'
permalink: _posts/:year/:month/:day/:title/
---

I have recently started to learn about parallel computing. In this blog post today, I will share a simple example of how to parallelize a molecular dynamics (MD) simulation using the Message Passing Interface (MPI).

<!--more-->

### What is Molecular Dynamics?
Molecular dynamics simulations model the motion of particles (atoms or molecules) by solving Newton's equations of motion. The forces between particles are typically described by empirical potential functions, such as the Lennard-Jones potential.

### Why Use MPI for Molecular Dynamics?
MPI allows us to distribute the computation across multiple processors, significantly speeding up simulations involving large numbers of particles. This is particularly important for MD simulations, which can be computationally intensive due to the need to calculate pairwise interactions between particles.

### Basic Molecular Dynamics Simulation Example with MPI
This code will calculate the energies and forces between particles and propagate the system over time.

```python
from mpi4py import MPI
import numpy as np

# Define constants
N_PARTICLES = 100  # Total number of particles
TIME_STEP = 0.01   # Time step for integration
NUM_STEPS = 100    # Number of time steps

# Initialize MPI environment
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Divide particles among processes
particles_per_process = N_PARTICLES // size
start_particle = rank * particles_per_process
end_particle = (rank + 1) * particles_per_process

if rank == size - 1:  # Last process handles any remaining particles
    end_particle = N_PARTICLES

# Initialize particle positions and velocities
positions = np.random.rand(N_PARTICLES, 3)
velocities = np.random.rand(N_PARTICLES, 3)

# Function to calculate Lennard-Jones potential energy
def lennard_jones_energy(r):
    sigma = 1.0
    epsilon = 1.0
    return 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)

# Function to calculate force between two particles
def calculate_force(position_i, position_j):
    r = np.linalg.norm(position_i - position_j)
    if r == 0:
        return np.zeros(3)
    force = 4 * (12 * (1 / r)**13 - 6 * (1 / r)**7) * (position_i - position_j) / r
    return force

# Main simulation loop
for step in range(NUM_STEPS):
    # Calculate forces for particles assigned to this process
    forces = np.zeros((end_particle - start_particle, 3))
    for i in range(start_particle, end_particle):
        for j in range(N_PARTICLES):
            if i != j:
                force = calculate_force(positions[i], positions[j])
                forces[i - start_particle] += force

    # Update velocities and positions using Verlet integration
    for i in range(start_particle, end_particle):
        velocities[i] += forces[i - start_particle] * TIME_STEP
        positions[i] += velocities[i] * TIME_STEP
    
    # Gather updated positions from all processes
    updated_positions = np.zeros((N_PARTICLES, 3))
    comm.Allgather(positions[start_particle:end_particle], updated_positions[start_particle:end_particle])
    positions = updated_positions
    
    # Print current state (optional)
    if rank == 0:
        print(f"Step {step}:")
        print(positions)
    
# Finalize MPI environment
MPI.Finalize()
```

## Explanation of the Code:
- **Initialization**: The code initializes an MPI environment and divides particles among processes.
- **Force Calculation**: It calculates the forces between particles using the Lennard-Jones potential.
- **Integration**: The code updates particle velocities and positions using a simplified version of the Verlet integration algorithm.
- **Communication**: Updated positions are gathered from all processes using `Allgather`.

## Running the Code:
To run this code, save it to a file (e.g., `md_mpi.py`) and execute it using `mpirun` with multiple processes:

```bash
mpirun -np 4 python md_mpi.py
```

This will distribute the simulation across 4 processes.

## Conclusion
This example demonstrates how MPI can be used to parallelize a basic molecular dynamics simulation. By distributing the computation across multiple processes, you can significantly speed up simulations involving large numbers of particles.

## Further Reading
- [MPI Official Documentation](https://www.mpi-forum.org/docs/)
- [Molecular Dynamics Tutorial](https://docs.matlantis.com/atomistic-simulation-tutorial/en/6_1_md-nve.html)

## Getting Started with MPI
1. **Install mpi4py**: Use pip to install the Python MPI library.
```bash
pip install mpi4py
```
2. **Install OpenMPI or MPICH**: Ensure you have an MPI implementation installed on your system.
3. **Run Your First MPI Program**: Use `mpirun` to execute your MPI scripts.
