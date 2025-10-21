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
page_modified: 2025-10-20
---

Developed a tracking tool to manage and monitor high-throughput Monte Carlo simulations using the gRASPA software package. The tool was required to be developed to efficiently generate the dataset needed for training an interpretable machine learning model (more details in [Relevant links](#relevant-links)). Since then, the tool has been used in a few other projects ranging from simply parsing the adsorbate number to complete adsorption isotherm plots. More details on the tool and its functionalities are available in the [GitHub repository](https://github.com/sbkashif/gRASPA_job_tracker).

<!--more-->

 A typical workflow involves setting up multiple simulation jobs with varying parameters across different compute nodes. The tracker keeps track of job statuses, retries failed simulations, and compiles results into a structured format for downstream analysis. The key idea is to control all the simulation and software settings from a single `config file` and ensure reproducibility.

Here is an example `config file` used to generate adsorption isotherms:
```yaml
# Project configuration
project:
  name: "coremof_parameter_matrix"  # Project name used for organizing data directories

# Output directory structure
output:
  base_dir: ${PROJECT_ROOT}/examples/data/${project.name}/  # Base directory for output

# Database configuration
database:
  path: ${PROJECT_ROOT}/examples/data/${project.name}/raw
  remote_url: None
  extract: true

# Batch settings
batch:
  size: 1  # Number of structures per batch
  max_concurrent_jobs: 50  # Maximum number of concurrent jobs
  strategy: custom_alphabetical  # Options: alphabetical, custom_alphabetical, size_based, random
  copy_files: false

# Parameter Matrix Configuration - NEW FEATURE
parameter_matrix:
  # Define parameter ranges
  parameters:
    temperature: [298, 313, 333]  # K
    pressure: [100000, 200000, 500000]  # Pa
    co2_molfraction: [0.15, 0.25, 0.35]  # CO2 mole fraction
    n2_molfraction: [0.85, 0.75, 0.65]   # N2 mole fraction (should sum to 1.0 with CO2)
  
  # How to combine parameters: 'all' for all combinations, 'custom' for specific combinations
  combinations: 'all'  # This will create 3x3x3x3 = 81 parameter combinations per batch
  
  # Alternative: use custom combinations
  # combinations: 'custom'
  # custom_combinations:
  #   - name: "low_temp_low_pressure"
  #     parameters:
  #       temperature: 298
  #       pressure: 100000
  #       co2_molfraction: 0.15
  #       n2_molfraction: 0.85
  #   - name: "high_temp_high_pressure"
  #     parameters:
  #       temperature: 333
  #       pressure: 500000
  #       co2_molfraction: 0.35
  #       n2_molfraction: 0.65

# Script paths
scripts:
  simulation: gRASPA_job_tracker.scripts.raspa_simulation
  analysis: gRASPA_job_tracker.scripts.raspa_analysis

# File templates with parameter substitution support
run_file_templates:
  simulation_input:
    file_path: ${PROJECT_ROOT}/templates/simulation.input
    variables:
      NumberOfInitializationCycles: 2000000
      NumberOfProductionCycles: 2000000
      MoviesEvery: 3000000
      # Parameter matrix values will be automatically substituted in simulation.input
      # The system will find lines that start with parameter names and replace their values
      # For example: "Temperature 298" will become "Temperature 313" for parameter combinations
      # CO2 and N2 mole fractions will be updated in their respective component sections

# Forcefield files
forcefield_files:
  force_field_mixing_rules: ${PROJECT_ROOT}/forcefields/N2-Forcefield/force_field_mixing_rules.def
  force_field: ${PROJECT_ROOT}/forcefields/N2-Forcefield/force_field.def
  pseudo_atoms: ${PROJECT_ROOT}/forcefields/N2-Forcefield/pseudo_atoms.def
  CO2: ${PROJECT_ROOT}/forcefields/N2-Forcefield/CO2.def
  N2: ${PROJECT_ROOT}/forcefields/N2-Forcefield/N2.def

# SLURM configuration - will be scaled for parameter matrix
slurm_config:
  account: bcvz-delta-gpu
  partition: gpuA100x4
  time: 8:00:00  # Increased time for parameter matrix jobs
  nodes: 1  # Will be automatically set to number of parameter combinations
  mem: 50GB

# Environment setup
environment_setup: |
  cd $SLURM_SUBMIT_DIR
  module load anaconda3_gpu
  source deactivate graspa
  export LD_LIBRARY_PATH=$HOME/software/gcc-13.3.0/lib64:$LD_LIBRARY_PATH
  export gRASPA_executable=$HOME/software/gRASPA/patch_Allegro/nvc_main.x
  source activate graspa
```

Following is a brief overview of the tool's interface and workflow (fetching all the informaion from the config file):
 - First, users will define a database of the structures to be simulated. For now, the package is tested only on RASPA and gRASPA software, and hence only with CIF format files.
 - Next, a splitting strategy is defined to divide the total number of simulations into smaller batches that can be run on different compute nodes. This helps in efficient resource utilization and parallel execution. A typical splitting strategy will be based on alphabetical order or random assignment.
 - Then, the package will automatically assign a compute node for each batch of structures based on the defined splitting strategy. A user-defined simulation environment (like software modules) will also be loaded in each node.
 - Finally, the simulation workflow will be performed on each batch, with the tracker monitoring job statuses, handling retries for failed jobs, and compiling results into a CSV file for easy analysis.

A more detailed schematic is available in the supplementary information of the preprint referred in the [relevant links](#relevant-links). I am not putting here since paper is under review and I am unsure about copyright tranfer policies of the journal.

 An example CSV file generated by the tracker is shown below:
 ```csv
 batch_id,job_id,param_combination_id,status,submission_time,completion_time,workflow_stage
26,20968283,B26_T473_N20_H21.0_NH30_P0.6210169418915616,RUNNING,2025-08-22 20:19:51,,simulation (cycle 103000)
26,20968304,B26_T473_N21.0_H20_NH30_P0.00011721022975334806,RUNNING,2025-08-22 20:19:52,,simulation (cycle 161000)
26,20968296,B26_T473_N20_H21.0_NH30_P148735.21072935118,RUNNING,2025-08-22 20:19:52,,simulation (cycle 100000)
26,20968293,B26_T473_N20_H21.0_NH30_P8531.678524172814,RUNNING,2025-08-22 20:19:52,,simulation (cycle 108000)
```

Further details on the simulations of a given batch can be referenced from the dedicated batch directory. Overall project directory structure is as follows:

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

The community is invited toexplore and contribute to the development of this gRASPA job tracker tool. Its modular design allows for easy extension to other simulation packages and workflows, making it a versatile solution for high-throughput computational studies.

<!-- Project links: GitHub repo and arXiv preprint -->
{% include referral_links.html %}

