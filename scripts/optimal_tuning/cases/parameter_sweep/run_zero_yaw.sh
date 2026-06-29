#!/bin/sh
#
#SBATCH --job-name="zero yaw" 
#SBATCH --partition=compute-p2
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem-per-cpu=2GB
#SBATCH --account=innovation
#SBATCH --mail-type=END

# Load necessary modules. The intel module is needed to run OpenFAST
# (libmkl_gf_lp64.so.2).
module load 2025
module load intel/oneapi-all
module load miniconda3

# If python buffers print statements it becomes a lot harder to debug. So let's
# not allow buffering for now.
export PYTHONUNBUFFERED=1

# OpenMDAO disables MPI when there is only 1 rank (ntasks=1), even though the
# DOE code path needs it to reach the multiprocessing-based OpenFAST
# parallelization. Force MPI to stay enabled.
export OPENMDAO_USE_MPI=1

# See: https://doc.dhpc.tudelft.nl/delftblue/Slurm-scheduler/#intel-mpi-job
export I_MPI_PMI_LIBRARY=/cm/shared/apps/slurm/current/lib64/libpmi2.so

# And run in the conda environment.
conda activate tip_clearance
echo "Python executable: $(which python)."
echo "Running weis_driver_zero_yaw.py now..."
srun python weis_driver_zero_yaw.py
conda deactivate
