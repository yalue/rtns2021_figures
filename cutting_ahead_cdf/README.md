Generating Data
---------------

The data in this directory was generated using `hip_plugin_framework`. From in
the main `hip_plugin_framework` directory, run `make`, then
`find configs/cutting_ahead_figure* -exec ./bin/runner {} \;`. The results will
be placed in the `results/` directory.

Drawing the CDF
---------------

The `view_times_cdf.py` script was also copied from `hip_plugin_framework`. It
was copied in order to make paper-specific modifications. To generate the plot
simply run it: `python view_times_cdf.py`.

NOTE: you may need to run it using Python 3!

