import os
import sys
from mpi4py import MPI
from weis import weis_main


this_dir = os.path.dirname(os.path.abspath(__file__))
wt_input = os.path.join(this_dir, "../../data/turbine_models/IEA-15-240-RWT.yaml")
modeling_options = os.path.join(this_dir, "modeling_options.yaml")
analysis_options = os.path.join(this_dir, "analysis_options.yaml")

# Works for simple runs or optimizations, not design_of_experiments.
# Also reduces the amount of DLC's so you cannot test whether you have allocated the
# correct amount of processors. See: set_modopt_test_runs()
test_run = False  

wt_opt, modeling_options, opt_options = weis_main(
    wt_input,
    modeling_options,
    analysis_options,
    test_run=test_run,
)

# Sometimes the job 'hangs' when it is complete due to an MPI process that is not
# closed.
# This approach didn't work. I got the error `Communicator (handle=44000000) being freed
# has 3 unmatched message(s)`.
# comm = MPI.COMM_WORLD
# comm.Barrier()
# MPI.Finalize()

# So we use the more forceful approach below.
comm = MPI.COMM_WORLD
comm.Barrier()
print("Terminating forcefully.")
sys.stdout.flush()  # Make sure all outputs are written
sys.stderr.flush()
os._exit(0)  # Terminate
