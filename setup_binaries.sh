#!/bin/sh
#
#SBATCH --job-name="setup openfast and rosco" 
#SBATCH --partition=compute 
#SBATCH --time=02:00:00 
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=2GB

# This batch script compiles the custom versions of OpenFAST and ROSCO that are
# used in this repository. It should take about 15-30 minutes or so.

# Store base directory
BASE_DIR=$(pwd)

echo "Starting setup process..."

# Let's first compile OpenFAST and ROSCO.
echo "Loading modules..."
module load 2025
module load cmake
module load intel/oneapi-all

# Compile OpenFAST.
echo "Compiling OpenFAST..."
cd "$BASE_DIR/src/openfast"
mkdir -p build
cd build
cmake ..
make -j8
make install

# Compile ROSCO.
echo "Compiling ROSCO..."
cd "$BASE_DIR/src/ROSCO/rosco/controller"
mkdir -p build
cd build
cmake ..
make -j8
make install


# Test OpenFAST.
echo ""
echo "Testing..."
cd "$BASE_DIR/src/openfast/install/bin"
./openfast -v

# We're done.
echo ""
echo "Done."
echo "OpenFAST path: $BASE_DIR/src/openfast/install/bin/openfast"
echo "ROSCO path: $BASE_DIR/src/ROSCO/rosco/lib/libdiscon.so"
