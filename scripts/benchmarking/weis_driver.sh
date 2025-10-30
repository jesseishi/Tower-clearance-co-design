#!/bin/sh
#
#SBATCH --job-name="weis-test" 
#SBATCH --partition=compute 
#SBATCH --time=01:30:00 
#SBATCH --ntasks=2 
#SBATCH --cpus-per-task=1 
#SBATCH --mem-per-cpu=2GB

# Load necessary modules. The intel module is needed to run OpenFAST
# (libmkl_gf_lp64.so.2).
module load 2025
module load intel/oneapi-all
module load miniconda3

# See: https://doc.dhpc.tudelft.nl/delftblue/Slurm-scheduler/#intel-mpi-job
export I_MPI_PMI_LIBRARY=/cm/shared/apps/slurm/current/lib64/libpmi2.so

# And run in the conda environment.
conda activate tip_clearance
srun python weis_driver.py
conda deactivate
