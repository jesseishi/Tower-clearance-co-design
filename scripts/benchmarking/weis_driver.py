import os
from weis import weis_main

this_dir = os.path.dirname(os.path.abspath(__file__))
wt_input = os.path.join(this_dir, '../../data/IEA-15-240-RWT.yaml')
modeling_options = os.path.join(this_dir, 'modeling_options.yaml')
analysis_options = os.path.join(this_dir, 'analysis_options.yaml')

wt_opt, modeling_options, opt_options = weis_main(
    wt_input,
    modeling_options,
    analysis_options,
)
