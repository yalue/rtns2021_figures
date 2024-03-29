Data and Figures for my RTNS'21 Paper
=====================================

This repository only really makes sense if you're reading the paper it
supports.  The paper can be found [here](https://www.cs.unc.edu/~otternes/papers/rtns2021.pdf).

Some Specifics
--------------

This assumes you're using python 3, with `matplotlib` and `numpy` available.
You'll also need the `hip_plugin_framework` and a Radeon VII GPU if you want to
try reproducing the results.  The `hip_plugin_framework` code can be found
[here](https://github.com/yalue/hip_plugin_framework).

 - The Table 1 data is located in the `worst_case_experiment/` directory. See
   the README in that directory for more information on how the data was
   generated.

 - The Figure 7 data is located in the `cutting_ahead_timelines/` directory.
   See the README in that directory for more information on how the data was
   generated.

 - Figure 9 is based on the data in the `cu_mask_scatterplot/` directory. See
   the README in that directory for more information on the data.

 - Table 2 is based on the data in the `striping_vs_not_table/` directory. As
   with the other subdirectories, see the README there for more information.

