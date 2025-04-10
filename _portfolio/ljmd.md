---
layout: portfolio_item
title: "Molecular Dynamics Simulation with Lennard-Jones Potential"
permalink: /portfolio/ljmd/
keywords: C++, molecular dynamics, Lennard-Jones potential, C++, simulation, unit testing
thumbnail: https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Graph_of_Lennard-Jones_potential.png/1599px-Graph_of_Lennard-Jones_potential.png?20201007144459
thumbnail_alt: "C++ Programming Language Logo"
thumbnail_credit: "Lennard-Jones potential graph, Wikimedia Commons"
thumbnail_credit_url: "https://commons.wikimedia.org/wiki/File:Graph_of_Lennard-Jones_potential.png"
languages: ["C++"]
---
<span class="attribution" style="color: gray; display: inline-block; margin-left: 0px;">Written with assistance from <a href="https://github.com/features/copilot" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/8/8a/GitHub_Copilot_logo.svg" class="logo" alt="GitHub Copilot" style="vertical-align: middle; margin-bottom: 3px;"/></a></span>

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sbkashif/lennard-jones-cpp) 





This project implements a molecular dynamics simulation framework using the Lennard-Jones potential to model particle interactions. Molecular Dynamics (MD) simulations are a powerful computational technique used in physics, chemistry, and materials science to study the physical movements of atoms and molecules.

<!--more-->

This project implements a basic MD engine that simulates particles interacting via the Lennard-Jones potential, which is commonly used to model noble gases and other simple fluids. The code is designed with a focus on modularity and extensibility, making it an excellent foundation for more complex simulations.

## Installation Guide

### Prerequisites

Before we begin, make sure you have the following installed on your system:

- C++17 compatible compiler (GCC, Clang, or MSVC)
- CMake 3.14 or higher
- Git (for cloning the repository)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/lennard-jones-cpp.git
   cd lennard-jones-cpp
   ```

2. **Create and enter build directory**

   ```bash
   mkdir -p build
   cd build
   ```

3. **Configure and build the project**

   ```bash
   cmake ..
   make
   ```

   This will compile the main executable `ljmd` along with the test programs.

## Running Unit Tests

The project includes comprehensive unit tests built with Google Test. After building the project, you can run the tests to ensure everything is working correctly.

### Vector Tests

These tests verify the functionality of the 3D vector class used in the simulation:

```bash
cd build/test
./vector_test
```

#### Results:

```
[==========] Running 4 tests from 1 test suite.
[----------] Global test environment set-up.
[----------] 4 tests from Vector3DTest
[ RUN      ] Vector3DTest.Construction
[       OK ] Vector3DTest.Construction (0 ms)
[ RUN      ] Vector3DTest.ArithmeticOperations
[       OK ] Vector3DTest.ArithmeticOperations (0 ms)
[ RUN      ] Vector3DTest.VectorProperties
[       OK ] Vector3DTest.VectorProperties (0 ms)
[ RUN      ] Vector3DTest.PeriodicBoundary
[       OK ] Vector3DTest.PeriodicBoundary (0 ms)
[----------] 4 tests from Vector3DTest (0 ms total)

[----------] Global test environment tear-down
[==========] 4 tests from 1 test suite ran. (0 ms total)
[  PASSED  ] 4 tests.
```

All tests for the Vector3D class have passed successfully, confirming that:
- Vector construction works correctly
- Arithmetic operations (addition, subtraction, etc.) function as expected
- Vector properties (norm, dot product, etc.) are calculated correctly
- Periodic boundary conditions are properly applied

### Particle Tests

These tests verify the functionality of the Particle class, which represents individual particles in the simulation:

```bash
cd build/test
./particle_test
```

#### Results:

```
[==========] Running 3 tests from 1 test suite.
[----------] Global test environment set-up.
[----------] 3 tests from ParticleTest
[ RUN      ] ParticleTest.Construction
[       OK ] ParticleTest.Construction (0 ms)
[ RUN      ] ParticleTest.Methods
[       OK ] ParticleTest.Methods (0 ms)
[ RUN      ] ParticleTest.Update
[       OK ] ParticleTest.Update (0 ms)
[----------] 3 tests from ParticleTest (0 ms total)

[----------] Global test environment tear-down
[==========] 3 tests from 1 test suite ran. (0 ms total)
[  PASSED  ] 3 tests.
```

All tests for the Particle class have passed successfully, confirming that:
- Particle objects are constructed correctly
- Methods to get and set particle properties work as expected
- The update mechanism for particle positions and velocities functions correctly

## Running a Simulation

Let's run a sample simulation to see the program in action.

```bash
cd build
./ljmd -n 125 -s 1000 -o 100
```

This runs a simulation with 125 particles for 1000 steps, outputting data every 100 steps.

### Simulation Results

The simulation ran with the following parameters:
- 125 particles
- Density: 0.8 (in reduced units)
- Initial temperature: 1.0 (in reduced units)
- Timestep: 0.001
- Cutoff radius: 2.5

#### Equilibration Phase

During the equilibration phase, the system stabilizes:

```
Starting equilibration phase...
Equilibration: 100/1000, T = 0.523727, E = -406.848
Equilibration: 200/1000, T = 0.717055, E = -406.845
Equilibration: 300/1000, T = 1.07157, E = -406.845
...
Equilibration: 1000/1000, T = 0.92201, E = -406.849
Equilibration completed.
```

The temperature fluctuates initially but eventually stabilizes around 0.92, which is close to the target temperature of 1.0. The total energy remains stable around -406.85 (in reduced units).

#### Production Phase

During the production phase, we collect data for analysis:

```
Step    50, T = 0.9570, E = -4.068482e+02, drift = 1.449238e-06
Step   100, T = 0.9507, E = -4.068487e+02, drift = 2.873342e-07
...
Step  5000, T = 0.9188, E = -4.068453e+02, drift = 8.592990e-06
```

The temperature fluctuates naturally around 0.95, while the total energy remains remarkably stable. The energy drift (a measure of energy conservation) stays below 1.5×10^-5 throughout the simulation, indicating excellent numerical stability.

#### Performance

The simulation completed in approximately 5.69 seconds for 5000 time steps with 125 particles, which is quite efficient for a small-scale simulation.

## Analysis of Results

### Energy Conservation

The total energy drift of 8.59×10^-6 over 5000 steps is extremely small (about 0.000002% of the total energy), indicating excellent energy conservation. This confirms that the velocity Verlet integrator is working correctly.

### Temperature Stability

The temperature fluctuates around 0.92-0.95, which is close to the target temperature of 1.0. These fluctuations are expected in the NVE ensemble where energy, not temperature, is conserved.

### System Stability

The simulation maintains stable particle interactions throughout the run, with no anomalies in energy or temperature. This suggests the Lennard-Jones potential and force calculations are implemented correctly.

## Visualization and Output Files

The simulation generates several output files:

- `trajectory.xyz`: Contains the positions of all particles at regular intervals, suitable for visualization with tools like VMD or OVITO
- `properties.dat`: Records system properties like temperature and energy over time
- `energy.dat`: Contains detailed energy components (kinetic, potential, total)
- `initial.xyz` and `final.xyz`: The starting and ending configurations of the system

## Extending the Simulation

The modular design makes it easy to extend this simulation. Some ideas for future enhancements include:

1. **Adding thermostats** - Implement Nose-Hoover or Berendsen thermostats for temperature control
2. **Different integrators** - Add alternatives to Velocity-Verlet, such as leapfrog or predictor-corrector methods
3. **Force field extensions** - Implement more complex potentials beyond Lennard-Jones
4. **Parallelization** - Add OpenMP or MPI support for faster simulations of larger systems

## Conclusion

The Lennard-Jones MD simulation project was an attempt to cement my understanding of MD simulation concepts, and getting used to unit testing in C++. The project successfully implements a basic MD engine with a focus on modularity and extensibility. The simulation runs efficiently, conserves energy, and produces stable results, making it a solid foundation for further exploration in molecular dynamics.