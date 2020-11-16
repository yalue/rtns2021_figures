# This script generates all of the data for the "worst practices" experiment
# in the paper. Run it while in the `hip_plugin_framework` directory, then copy
# the .json files from `hip_plugin_framework/results/`.
import copy
import json
import subprocess
import time

def generate_configs():
    """ Returns a list of JSON configs, containing one JSON string per
    experiment in the paper. """
    # Start by defining a base config for MM1024 and MM256. We'll copy these
    # and modify them as necessary.
    mm1024_config = {
        "label": "MM1024",
        "log_name": "./results/mm1024_isolated.json",
        "filename": "./bin/matrix_multiply.so",
        "thread_count": 1024,
        "block_count": 1,
        "additional_info": {
            "matrix_width": 1024,
            "skip_copy": True
        }
    }
    mm256_config = {
        "label": "MM256",
        "log_name": "./results/mm256_isolated.json",
        "filename": "./bin/matrix_multiply.so",
        "thread_count": 256,
        "block_count": 1,
        "additional_info": {
            "matrix_width": 1024,
            "skip_copy": True
        }
    }
    # Create a couple explicit "isolated" plugin configs in case we want to
    # include "isolated" curves on later plots.
    mm1024_isolated = copy.deepcopy(mm1024_config)
    mm1024_isolated["label"] = "MM1024 (isolated)"
    mm256_isolated = copy.deepcopy(mm256_config)
    mm256_isolated["label"] = "MM256 (isolated)"
    to_return = []
    # We'll also copy and modify this top-level config, generally only to
    # change the scenario name.
    overall_config = {
        "name": "MM1024 and MM256 Isolated",
        "max_iterations": 0,
        "max_time": 10.0,
        "gpu_device_id": 0,
        "pin_cpus": True,
        "do_warmup": True,
        "omit_block_times": True,
        "sync_every_iteration": False,
        "plugins": [mm1024_config]
    }
    to_return.append(json.dumps(overall_config))
    # Add the other plot of MM256 isolated to the scenario.
    overall_config["plugins"] = [mm256_config]
    to_return.append(json.dumps(overall_config))

    # Now we'll make a plot of MM1024 and MM256, running at the same time.
    overall_config["name"] = "MM1024 vs MM256, Full GPU Sharing"
    mm1024_config["log_name"] = "./results/mm1024_full_shared.json"
    mm256_config["log_name"] = "./results/mm256_full_shared.json"
    overall_config["plugins"] = [mm1024_config, mm256_config]
    to_return.append(json.dumps(overall_config))

    # Now make MM1024 and MM256 run at the same time, but on partitions. We're
    # "cheating" a little here for dramatic effect--we already know this is a
    # good CU mask, but readers may not.
    cu_mask_A = "10" * 30
    cu_mask_B = "01" * 30
    mm1024_config["compute_unit_mask"] = cu_mask_A
    mm1024_config["label"] = "MM1024, 30 CU Partition"
    mm1024_config["log_name"] = "./results/mm1024_equal_partitioned.json"
    mm256_config["compute_unit_mask"] = cu_mask_B
    mm256_config["label"] = "MM256, 30 CU Partition"
    mm256_config["log_name"] = "./results/mm256_equal_partitioned.json"
    overall_config["name"] = "MM1024 vs MM256, Evenly Partitioned Sharing"
    overall_config["plugins"] = [mm1024_config, mm256_config]
    to_return.append(json.dumps(overall_config))

    # Now do the same thing, except change MM1024's CU mask to include one MORE
    # CU--shared with MM256's partition.
    cu_mask_A = "10" * 29 + "11"
    mm1024_config["compute_unit_mask"] = cu_mask_A
    mm1024_config["label"] = "MM1024, 31 CU Partition"
    mm1024_config["log_name"] = "./results/mm1024_unequal_partitioned.json"
    mm256_config["log_name"] = "./results/mm256_unequal_partitioned.json"
    overall_config["name"] = "MM1024 vs MM256, Uneven Partitioned Sharing"
    overall_config["plugins"] = [mm1024_config, mm256_config]
    to_return.append(json.dumps(overall_config))

    return to_return

if __name__ == "__main__":
    configs = generate_configs()
    for i in range(len(configs)):
        print("Running experiment %d of %d" % (i + 1, len(configs)))
        config = configs[i]
        process = subprocess.Popen(["./bin/runner", "-"],
            stdin=subprocess.PIPE)
        process.communicate(input=config)
        print("Sleeping a bit.\n")
        time.sleep(2.0)

