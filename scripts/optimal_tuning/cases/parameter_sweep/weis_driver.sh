#!/bin/sh
#
#SBATCH --job-name="weis" 
#SBATCH --partition=compute-p2
#SBATCH --time=12:00:00
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=60
#SBATCH --mem-per-cpu=2GB
#SBATCH --account=research-me-dcsc
#SBATCH --mail-type=ALL

# Load necessary modules. The intel module is needed to run OpenFAST
# (libmkl_gf_lp64.so.2).
module load 2025
module load intel/oneapi-all
module load miniconda3

# If python buffers print statements it becomes a lot harder to debug. So let's
# not allow buffering for now.
export PYTHONUNBUFFERED=1

# See: https://doc.dhpc.tudelft.nl/delftblue/Slurm-scheduler/#intel-mpi-job
export I_MPI_PMI_LIBRARY=/cm/shared/apps/slurm/current/lib64/libpmi2.so

# And run in the conda environment.
conda activate tip_clearance
echo "Python executable: $(which python)."
echo "Running weis_driver.py now..."
srun python weis_driver.py
conda deactivate
