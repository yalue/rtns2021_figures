import json
import numpy

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

def print_table_row(filename, cu_mask, competitor_mask, scenario):
    stats = None
    with open(filename) as f:
        plugin = json.loads(f.read())
        times = get_times(plugin)
        stats = compute_stats(times)
    print("%s & %s & %s & %.3f & %.3f & %.3f & %.3f & %.3f \\\\" % (scenario, cu_mask,
        competitor_mask, stats[0], stats[1], stats[2], stats[3], stats[4]))
    return None

print(r'\hline')
print(r'Scenario & \mmsbig{} CU Mask & \mmsmall{} CU Mask & Min & Max & Median & Arith. Mean & Std. Dev. \\')
print(r'\hline')
print_table_row("./1024_vs_256_evenly_partitioned.json", r'\texttt{1010}...\texttt{101\textbf{0}}', r'\texttt{0101}...\texttt{0101}', "Striped, Equal Partitions")
print_table_row("./1024_vs_256_unevenly_partitioned.json", r'\texttt{1010}...\texttt{101\textbf{1}}', r'\texttt{0101}...\texttt{0101}', "Striped, Unequal Partitions")
print_table_row("./mm1024_unstriped_even.json", r'\texttt{1111}...\texttt{000\textbf{0}}', r'\texttt{0000}...\texttt{1111}', "Unstriped, Equal Partitions")
print_table_row("./mm1024_unstriped_uneven.json", r'\texttt{1111}...\texttt{000\textbf{1}}', r'\texttt{0000}...\texttt{1111}', "Unstriped, Unequal Partitions")
print(r'\hline')

