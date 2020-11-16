import argparse
import glob
import itertools
import json
import matplotlib.pyplot as plot
import numpy
import re
import sys

def convert_values_to_cdf(values):
    """Takes a 1-D list of values and converts it to a CDF representation. The
    CDF consists of a vector of times and a vector of percentages of 100."""
    if len(values) == 0:
        return [[], []]
    values.sort()
    total_size = float(len(values))
    current_min = values[0]
    count = 0.0
    data_list = [values[0]]
    ratio_list = [0.0]
    for v in values:
        count += 1.0
        if v > current_min:
            data_list.append(v)
            ratio_list.append((count / total_size) * 100.0)
            current_min = v
    data_list.append(values[-1])
    ratio_list.append(100)
    return [data_list, ratio_list]

def compute_stats(data):
    """ Returns the min, max, med, mean, and stddev (in that order) of the
    given data. """
    data.sort()
    med = data[int(len(data) / 2)]
    mean = numpy.mean(data)
    std = numpy.std(data)
    return data[0], data[-1], med, mean, std

def get_times(plugin):
    """ Returns an array of the plugin's "execute_times", converted to ms. """
    to_return = []
    k = "execute_times"
    for t in plugin["times"]:
        if not k in t:
            continue
        # End time - start time, converted to ms.
        to_return.append((t[k][1] - t[k][0]) * 1000.0)
    return to_return

def get_line_dashes(label):
    """ Returns the line style that we'll use across all plots for a given
    label. """

    iso = "Isolated"
    full = "Full GPU Sharing"
    even = "Evenly Partitioned"
    bad = "Partitioned, w/ Additional Shared CU"
    if label == iso:
        return {"dashes": [1, 0]}
    elif label == full:
        return {"dashes": [3, 1, 3, 1]}
    elif label == even:
        return {"dashes": [1, 1, 1, 1]}
    elif label == bad:
        return {"dashes": [3, 1, 1, 1]}
    print("Unknown label: " + str(label))
    exit(1)

def add_plot_padding(axes):
    """Takes matplotlib axes, and adds some padding so that lines close to
    edges aren't obscured by tickmarks or the plot border."""
    y_limits = axes.get_ybound()
    y_range = y_limits[1] - y_limits[0]
    y_pad = y_range * 0.05
    x_limits = axes.get_xbound()
    x_range = x_limits[1] - x_limits[0]
    x_pad = x_range * 0.05
    axes.set_ylim(y_limits[0] - y_pad, y_limits[1] + y_pad)
    axes.set_xlim(x_limits[0] - x_pad, x_limits[1] + x_pad)
    axes.xaxis.set_ticks(numpy.arange(x_limits[0], x_limits[1] + x_pad,
        x_range / 5.0))
    axes.yaxis.set_ticks(numpy.arange(y_limits[0], y_limits[1] + y_pad,
        y_range / 5.0))

def generate_plot(data, name):
    """ Takes a list of processed data elements and returns a figure, with the
    given title, of a CDF plot. """
    figure = plot.figure()
    figure.canvas.set_window_title(name)
    axes = figure.add_subplot(1, 1, 1)
    axes.autoscale(enable=True, axis="both", tight=True)
    for i in range(len(data)):
        d = data[i]
        cdf = d["cdf"]
        style_setting = get_line_dashes(d["label"])
        axes.plot(cdf[0], cdf[1], label=d["label"], lw=2.0, color="k",
            **style_setting)
    add_plot_padding(axes)
    axes.set_xlabel("Time (milliseconds)")
    axes.set_ylabel("% <= X")
    legend = plot.legend(loc=9)
    #legend.draggable()
    legend.set_draggable(True)
    return figure

def get_data_list():
    """ Returns a list of data from parsed JSON files, computing stats and CDFs
    for each file. """
    iso = "Isolated"
    full = "Full GPU Sharing"
    even = "Evenly Partitioned"
    bad = "Partitioned, w/ Additional Shared CU"
    c1 = "MM1024 (vs. MM1024)"
    c2 = "MM1024 (vs. MM256)"
    c3 = "MM256 (vs. MM256)"
    c4 = "MM256 (vs. MM1024)"

    to_return = [
        # 0
        {"label": iso, "file": "1024_isolated.json", "category": "MM1024 Isolated"},
        # 1
        {"label": iso, "file": "256_isolated.json", "category": "MM256 Isolated"},
        # 2
        {"label": full, "file": "1024_vs_1024_full_shared.json", "category": c1},
        # 3
        {"label": even, "file": "1024_vs_1024_evenly_partitioned.json", "category": c1},
        # 4
        {"label": bad, "file": "1024_vs_1024_unevenly_partitioned.json", "category": c1},
        # 5
        {"label": full, "file": "1024_vs_256_full_shared.json", "category": c2},
        # 6
        {"label": even, "file": "1024_vs_256_evenly_partitioned.json", "category": c2},
        # 7
        {"label": bad, "file": "1024_vs_256_unevenly_partitioned.json", "category": c2},
        # 8
        {"label": full, "file": "256_vs_256_full_shared.json", "category": c3},
        # 9
        {"label": even, "file": "256_vs_256_evenly_partitioned.json", "category": c3},
        # 10
        {"label": bad, "file": "256_vs_256_unevenly_partitioned.json", "category": c3},
        # 11
        {"label": full, "file": "256_vs_1024_full_shared.json", "category": c4},
        # 12
        {"label": even, "file": "256_vs_1024_evenly_partitioned.json", "category": c4},
        # 13
        {"label": bad, "file": "256_vs_1024_unevenly_partitioned.json", "category": c4},
    ]

    # Parse the data, compute stats and CDFs
    for i in range(len(to_return)):
        with open(to_return[i]["file"]) as f:
            to_return[i]["data"] = json.loads(f.read())
        times = get_times(to_return[i]["data"])
        to_return[i]["times"] = times
        to_return[i]["stats"] = compute_stats(times)
        to_return[i]["cdf"] = convert_values_to_cdf(times)

    return to_return

def show_plots(data):
    """ Generates and displays the 4 CDF plots. """
    # Some of this data is reordered slightly so that the legend is always in
    # the order of the curves from left to right.
    plot1_data = [data[0], data[2], data[3], data[4]]
    # 1024-vs-256, where partitioned is faster
    plot2_data = [data[0], data[6], data[5], data[7]]
    plot3_data = [data[1], data[8], data[9], data[10]]
    # In this plot, vs. 1024 is faster (?? but consistently) than isolated.
    plot4_data = [data[11], data[1], data[12], data[13]]
    figures = []
    figures.append(generate_plot(plot1_data, "MM1024 (vs. MM1024)"))
    plot.subplots_adjust(bottom=0.35)
    figures.append(generate_plot(plot2_data, "MM1024 (vs. MM256)"))
    plot.subplots_adjust(bottom=0.35)
    figures.append(generate_plot(plot3_data, "MM256 (vs. MM256)"))
    plot.subplots_adjust(bottom=0.35)
    figures.append(generate_plot(plot4_data, "MM256 (vs. MM1024)"))
    plot.subplots_adjust(bottom=0.35)
    plot.show()
    return None

def print_table(data):
    print(r'Scenario & Partitioning & \# Samples & Min & Max & Median & Arith. Mean & Std. Dev. \\')
    print(r'\hline')
    for d in data:
        print("% Category: " + d["category"])
        v = d["stats"]
        n = len(d["times"])
        print(" & %s & %d & %.3f & %.3f & %.3f & %.3f & %.3f \\\\" % (d["label"], n,
            v[0], v[1], v[2], v[3], v[4]))
    print(r'\hline')

if __name__ == "__main__":
    data = get_data_list()
    show_plots(data)
    print_table(data)

