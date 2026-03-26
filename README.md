# Tower clearance co-design

This repository has been used towards the following publications:

1. "Increasing the blade tip-to-tower clearance using individual pitch control",
  Jesse I.S. Hummel, Jens Kober, Sebastiaan P. Mulders, Torque 2026, *accepted*

## Motivation
The design of large, flexible wind turbines is highly driven by the tip-to-tower
clearance constraint. Alleviating this constraint using pitch control could
enable lighter or larger blades that still satisfy design constraints.
Conventionally, the thrust of the rotor is limited by collective pitch control
to reduce the bending of the blades using peak shaving. However, individual
pitch control (IPC) could instead tilt the rotor backward, having a similar
effect on tower clearance but a smaller effect on annual energy production
because the total thrust remains unchanged. In [1], we develop two tower
clearance IPC controllers: a "free yaw" variant that achieves the required tower
clearance with the minimal required control action, and a "zero yaw" variant
that uses additional control effort to reduce the additional blade fatigue. In
future work, we aim to explore more of the design space and integrate these
controllers in a control co-design framework.

## Overview
This repository is structured as follows:

- `data`: All simulation results.
- `scripts`: All scripts used to generate and postprocess simulation results.
- `src`: Submodules
  - `/openfast`: OpenFAST submodule. Adjusted to output the blade tip deflection
    in the avrswap.
  - `/ROSCO`: ROSCO submodule. Adjusted with the tower clearance IPC
    controllers.
  - `/WEIS`: WEIS submodule. Adjusted to calculate the worst-case tower
    clearance over all simulations and be able to interact with our new ROSCO
    controllers.


## Installation
The controllers are implemented in ROSCO and are used here with custom versions
of OpenFAST and WEIS. These repositories are included as submodules. To clone
everything, run `git clone --recurse-submodules
https://github.com/jesseishi/Tower-clearance-co-design.git`.

Further installation depends on your platform. For the DelftBlue HPC, we have
made some utility shell scripts:

1. Submit [setup_binaries_delftblue.sh](setup_binaries_delftblue.sh) as a batch
   job, using `sbatch setup_binaries_delftblue.sh`. This will compile the custom
   version of OpenFAST and ROSCO as a batch job with 8 cores.
2. Run [setup_conda_delftblue.sh](setup_conda_delftblue.sh) on the login node.
   This will set up the `tip_clearance` conda environment. To run it, you first
   need to give it execution permissions with `chmod +x
   setup_conda_delftblue.sh`, and then run `./setup_conda_delftblue.sh`.
