# Tower clearance co design

## Installation
Since we are using custom versions of ROSCO, OpenFAST, and WEIS. They are
included as submodules. Clone the whole repository using `git clone
--recurse-submodules
https://github.com/jesseishi/Tower-clearance-co-design.git`.

Further installation depends on your platform. For the DelftBlue HPC (add
citation), we have made some utility shell scripts:

1. Submit [setup_binaries_delftblue.sh](setup_binaries_delftblue.sh) as a batch job, using `sbatch setup_binaries.sh`. This will
   compile the custom version of OpenFAST and ROSCO as a batch job with 8 cores.
2. Run [setup_conda_delftblue.sh](setup_conda_delftblue.sh) on the login node. This will setup the
   `tip_clearance` conda environment. To run it, you first need to give it
   execution permissions with `chmod +x setup_conda.sh`, and then run `./setup_conda.sh`.

## Notes

- When running on WSL with mpi. Setting `export OMP_NUM_THREADS=1` can help avoid issues
  with WSL. This fixed issues for me when running `mpiexec -n 8 python weis_driver.py`
