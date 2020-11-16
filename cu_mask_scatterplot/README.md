Generating Data
---------------

This data was generated using `hip_plugin_framework/scripts/test_cu_mask.py`.
The script was run twice (both times on the same Radeon VII GPU). From the
`hip_plugin_framework` base directory:

 - `python scripts/test_cu_mask.py --stripe_width 1`

 - `python scripts/test_cu_mask.py --stripe_width 4`

If the tests ever hang, they can be resumed by passing the `--start_count` flag
to the script, with the number of active CUs to resume the test with. If you're
using a GPU with a different number of CUs (the Radeon VII has 60), then you
should specify the total number of CUs on your GPU using the `--cu_count` flag.

When both scripts have run, they should have generated a bunch of files (one
per CU per stripe width, e.g. 120 for both stripe widths on a 60-CU GPU), in
the `results/` directory. Copy them to this directory.

Generating the Plots
--------------------

Run the `view_scatterplots.py` script in this directory to generate the
scatterplots.  It was copied and modified from the `view_scatterplots.py`
script in the `hip_plugin_framework` repo.

