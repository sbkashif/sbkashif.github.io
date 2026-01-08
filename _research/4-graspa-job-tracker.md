---
layout: research_item
title: High-throughput Monte Carlo simulations using gRASPA
thumbnail: assets/images/graspa-tracker-csv.png
codes:
  - url: "https://github.com/sbkashif/gRASPA_job_tracker"
    title: "gRASPA_job_tracker"
    thumbnail: assets/images/github-logo.svg
    description: "Refer to the GitHub repository for detailed installation instructions and usage guidelines."
preprints:
  - url: "https://arxiv.org/abs/2509.15908"
    title: "Interpretable Nanoporous Materials Design with Symmetry-Aware Networks"
    thumbnail: assets/images/arxiv-logo.svg
    description: "Check the methods and supplementary information sections for details on the gRASPA job tracker."
date_created: 2025-04-20
last_modified: 2025-10-23
---

Developed a tracking tool to manage and monitor high-throughput Monte Carlo simulations using the gRASPA software package. The tool was created to efficiently generate the datasets needed for training an interpretable machine learning model (more details in [Relevant links](#relevant-links)). Since then, the tool has been used in various other projects, ranging from parsing adsorbate numbers to generating complete adsorption isotherm plots. More details on the tool and its functionalities are available in the [GitHub repository](https://github.com/sbkashif/gRASPA_job_tracker).

<!--more-->

A typical workflow involves setting up multiple simulation jobs with varying parameters across different compute nodes. The tracker monitors job statuses, retries failed simulations, and compiles results into a structured format for downstream analysis. The key objective is to control all simulation and software settings from a single `config file` to ensure reproducibility.

Here is an example `config file` used to generate adsorption isotherms:
```yaml
# Project configuration
project:
  name: "coremof_parameter_matrix"  # Unique identifier for data organization

# Output directory structure
output:
  base_dir: ${PROJECT_ROOT}/examples/data/${project.name}/  # Root directory for results

# Database configuration
database:
  path: ${PROJECT_ROOT}/examples/data/${project.name}/raw
  remote_url: None
  extract: true

# Batch settings
batch:
  size: 1  # Number of structures processed per batch
  max_concurrent_jobs: 50  # Limit for simultaneous job submissions
  strategy: custom_alphabetical  # Sorting: alphabetical, custom_alphabetical, size_based, or random
  copy_files: false

# Parameter Matrix Configuration - NEW FEATURE
parameter_matrix:
  # Define simulation parameter ranges
  parameters:
    temperature: [298, 313, 333]  # K
    pressure: [100000, 200000, 500000]  # Pa
    co2_molfraction: [0.15, 0.25, 0.35]  # CO2 mole fraction
    n2_molfraction: [0.85, 0.75, 0.65]   # N2 mole fraction (binary mixture)
  
  # Generation logic: 'all' for Cartesian product, 'custom' for explicit pairs
  combinations: 'all'  # Generates 81 unique combinations (3^4) per batch
  
  # Example for explicit combinations:
  # combinations: 'custom'
  # custom_combinations:
  #   - name: "low_temp_low_pressure"
  #     parameters:
  #       temperature: 298
  #       pressure: 100000
  #       co2_molfraction: 0.15
  #       n2_molfraction: 0.85

# Executable script paths
scripts:
  simulation: gRASPA_job_tracker.scripts.raspa_simulation
  analysis: gRASPA_job_tracker.scripts.raspa_analysis

# File templates with dynamic parameter substitution
run_file_templates:
  simulation_input:
    file_path: ${PROJECT_ROOT}/templates/simulation.input
    variables:
      NumberOfInitializationCycles: 2000000
      NumberOfProductionCycles: 2000000
      MoviesEvery: 3000000
      # Values from the parameter matrix are automatically injected into simulation.input.
      # The engine replaces lines starting with parameter keys (e.g., "Temperature").

# Forcefield definitions
forcefield_files:
  force_field_mixing_rules: ${PROJECT_ROOT}/forcefields/N2-Forcefield/force_field_mixing_rules.def
  force_field: ${PROJECT_ROOT}/forcefields/N2-Forcefield/force_field.def
  pseudo_atoms: ${PROJECT_ROOT}/forcefields/N2-Forcefield/pseudo_atoms.def
  CO2: ${PROJECT_ROOT}/forcefields/N2-Forcefield/CO2.def
  N2: ${PROJECT_ROOT}/forcefields/N2-Forcefield/N2.def

# SLURM scheduler configuration
slurm_config:
  account: bcvz-delta-gpu
  partition: gpuA100x4
  time: 8:00:00  # Walltime allocated for parameter matrix sweep
  nodes: 1       # Scaled automatically based on combination count
  mem: 50GB

# Environment and dependency setup
environment_setup: |
  cd $SLURM_SUBMIT_DIR
  module load anaconda3_gpu
  source deactivate graspa
  export LD_LIBRARY_PATH=$HOME/software/gcc-13.3.0/lib64:$LD_LIBRARY_PATH
  export gRASPA_executable=$HOME/software/gRASPA/patch_Allegro/nvc_main.x
  source activate graspa
```

Below is a brief overview of the tool's interface and workflow:
- First, users define a database of the structures to be simulated. Currently, the package is tested only with the RASPA and gRASPA software; therefore, it supports only the CIF file format.
- Next, a splitting strategy is defined to divide the total number of simulations into smaller batches for distribution across different compute nodes. This ensures efficient resource utilization and parallel execution. Typical strategies include alphabetical order or random assignment.
- The package then automatically assigns a compute node to each batch based on the defined strategy. A user-defined simulation environment (such as specific software modules) is also loaded onto each node.
- Finally, the simulation workflow is executed for each batch. The tracker monitors job statuses, handles retries for failed jobs, and compiles results into a CSV file for streamlined analysis.

All the workflow logic is driven by a single `config file`, as shown above. The tool generates the necessary job scripts and batch files while organizing the output data into a structured directory format.

A more detailed schematic is available in the supplementary information of the preprint referenced in the [relevant links](#relevant-links). It is not included here as the paper is currently under review, and I am ensuring compliance with the journal's copyright transfer policies.

Further details regarding the simulations for a specific batch can be found within the dedicated batch directory. The overall project directory structure is organized as follows:

```txt
{PROJECT_NAME}/
├── data/
│   ├── raw/                # Original database files
│   ├── batches/            # Batch CSV files (same as standard)
│   │   ├── batch_1.csv     # Contains single CIF file per batch
│   │   ├── batch_2.csv
│   │   └── ...
│   ├── job_logs/           # Individual parameter combination logs
│   │   ├── batch_1_param_0_%j.out
│   │   ├── batch_1_param_1_%j.out
│   │   ├── batch_1_param_2_%j.out
│   │   └── ...
│   ├── job_status.csv      # Enhanced tracking with param_combination_id
│   ├── job_scripts/        # Individual job scripts per parameter combination
│   │   ├── job_batch_1_param_0.sh
│   │   ├── job_batch_1_param_1.sh
│   │   ├── job_batch_1_param_2.sh
│   │   └── ...
│   ├── parameter_matrix.json # Generated parameter combinations
│   └── results/            # Parameter-specific result directories
│       ├── B1_T298_P100000_CO20.15_N20.85/    # Batch 1, Parameter combination 0
│       │   ├── cif_file_list.txt
│       │   ├── simulation/
│       │   │   ├── exit_status.log
│       │   │   └── [simulation results]
│       │   ├── analysis/
│       │   │   ├── exit_status.log
│       │   │   └── [analysis results]
│       │   └── exit_status.log
│       ├── B1_T298_P100000_CO20.15_N20.75/    # Batch 1, Parameter combination 1
│       │   ├── cif_file_list.txt
│       │   ├── simulation/
│       │   └── analysis/
│       ├── B1_T298_P100000_CO20.15_N20.65/    # Batch 1, Parameter combination 2
│       │   └── ...
│       ├── B2_T298_P100000_CO20.15_N20.85/    # Batch 2, Parameter combination 0
│       │   └── ...
│       └── ...                                # Up to thousands of parameter combinations
```

As simulations are submitted and executed, the job tracker maintains a comprehensive CSV file (`job_status.csv`) that logs the status of every parameter combination for each batch. This file includes details such as job IDs, parameter combinations, submission and completion timestamps, and current workflow stages. An example snippet of the `job_status.csv` file is shown below:

```csv
 batch_id,job_id,param_combination_id,status,submission_time,completion_time,workflow_stage
26,20968283,B26_T473_N20_H21.0_NH30_P0.6210169418915616,RUNNING,2025-08-22 20:19:51,,simulation (cycle 103000)
26,20968304,B26_T473_N21.0_H20_NH30_P0.00011721022975334806,RUNNING,2025-08-22 20:19:52,,simulation (cycle 161000)
26,20968296,B26_T473_N20_H21.0_NH30_P148735.21072935118,RUNNING,2025-08-22 20:19:52,,simulation (cycle 100000)
26,20968293,B26_T473_N20_H21.0_NH30_P8531.678524172814,RUNNING,2025-08-22 20:19:52,,simulation (cycle 108000)
```


The community is invited to explore and contribute to the development of the gRASPA job tracker. Its modular design allows for easy extension to other simulation packages and workflows, making it a versatile solution for high-throughput computational studies.

<!-- Project links: GitHub repo and arXiv preprint -->
{% include referral_links.html %}

