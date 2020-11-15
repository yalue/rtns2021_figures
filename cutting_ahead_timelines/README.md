Generating Data
---------------

The data in this directory was generated using `hip_plugin_framework`. From in
the main `hip_plugin_framework` directory, run `make`, then
`find configs/cutting_ahead_timeline* -exec ./bin/runner {} \;`. The results
will be placed in the `results/` directory.

For best results, I've found that it's best to run this shortly after rebooting
the system and killing X. The GPU's clock, used to determine the start and end
of blocks, seems to produce strange results if the GPU has been running for a
while, leading to odd-looking holes in the timeline.

Drawing the Timelines
---------------------

The `view_timelines.py` script was also copied from `hip_plugin_framework`. It
was copied in order to make paper-specific modifications that weren't part of
the original, committed version. To generate the plots, just run:
`python view_timelines.py -z`.

