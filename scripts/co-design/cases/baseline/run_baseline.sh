#!/bin/bash
#
#SBATCH --job-name="baseline"
#SBATCH --partition=rome
#SBATCH --time=20:00:00
#SBATCH -N 1
#SBATCH --tasks-per-node 128
#SBATCH --requeue
#SBATCH --mail-type=END
#SBATCH --mail-user=j.i.s.hummel@tudelft.nl

# Load necessary modules. The intel module is needed to run OpenFAST
# (libmkl_gf_lp64.so.2).
module load 2025
module load intel/2025b
module load Miniconda3/25.5.1-1

# Fix miniconda error.
eval "$(conda shell.bash hook)"

# If python buffers print statements it becomes a lot harder to debug. So let's
# not allow buffering for now.
export PYTHONUNBUFFERED=1

# And run in the conda environment.
conda activate tip_clearance
echo "Python executable: $(which python)."
echo "Running weis_driver.py now..."
# srun python weis_driver.py
mpiexec -n 128 python weis_driver.py
conda deactivate
