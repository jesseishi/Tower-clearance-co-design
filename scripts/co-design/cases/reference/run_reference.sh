#!/usr/bin/bash
#
#SBATCH --job-name="reference" 
#SBATCH --partition=compute-p2
#SBATCH --time=05:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=2GB
#SBATCH --account=innovation
#SBATCH --mail-type=END

# Load necessary modules. The intel module is needed to run OpenFAST
# (libmkl_gf_lp64.so.2).
module load 2026 cpu
module load intel/oneapi-all
module load miniconda3

# If python buffers print statements it becomes a lot harder to debug. So let's
# not allow buffering for now.
export PYTHONUNBUFFERED=1

export OPENMDAO_USE_MPI=0

# And run in the conda environment.
conda activate tip_clearance
echo "Python executable: $(which python)."
echo "Running weis_driver.py now..."
srun python weis_driver.py
conda deactivate
