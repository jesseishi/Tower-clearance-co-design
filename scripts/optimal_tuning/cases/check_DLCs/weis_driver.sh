#!/bin/sh
#
#SBATCH --job-name="weis" 
#SBATCH --partition=memory
#SBATCH --time=24:00:00 
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=15GB
#SBATCH --account=innovation
#SBATCH --mail-type=ALL

# TODO: Check how to set ntasks and cpus-per-task for this type of simulation
# (many simulations for 1 setting). On the other hand, I needed the special
# memory partition because I got an out-of-memory error with 8 GB available. Ah
# yeah, if the simulations are parallel on 64 cores I also get more memory for
# postprocessing (which happens on 1 core I think).

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
