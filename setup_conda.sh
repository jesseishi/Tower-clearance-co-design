#!/bin/sh

# This script should be run from the login node. Don't run it on a compute node
# because they don't have access to the internet. It takes some time to run
# (about one hour or so?).
# To run it you likely first need to give it execute permissions with.
# chmod +x setup_conda.sh

# Load the necessary modules. Compilation modules are needed because ROSCO also
# builds the controller when installing the Python package.
module load 2025
module load cmake
module load intel/oneapi-all
module load miniconda3

# Store base directory
BASE_DIR=$(pwd)

# Set up the conda environment.
echo "Setting up conda environment..."
cd "$BASE_DIR"
module load miniconda3
conda config --add channels conda-forge

# Check if environment exists and create/update accordingly
if conda env list | grep -q "^tip_clearance "; then
    echo "Environment tip_clearance already exists, activating it..."
    conda activate tip_clearance
else
    echo "Creating new environment tip_clearance..."
    conda create -y --name tip_clearance
    conda activate tip_clearance
fi

# Let's first install all the dependencies.
# The ROSCO environment.yml doesn't include pip but relies on it. To get the
# correct version of everything it's better to start with WEIS.
echo "Installing WEIS dependencies..."
cd "$BASE_DIR/src/WEIS"
conda env update --file environment.yml

echo "Installing ROSCO dependencies..."
cd "$BASE_DIR/src/ROSCO"
conda env update --file environment.yml

# Other dependencies not listed in either environment.yml.
echo "Installing other dependencies..."
conda install -y mpi4py

# Now install ROSCO and WEIS.
echo "Installing ROSCO package..."
cd "$BASE_DIR/src/ROSCO"
pip install -e . --no-deps

echo "Installing WEIS package..."
cd "$BASE_DIR/src/WEIS"
pip install -e . --no-deps

# Deactivate the conda environment.
conda deactivate

echo ""
echo "Conda environment 'tip_clearance' is set up."
echo "Activate with: conda activate tip_clearance"
