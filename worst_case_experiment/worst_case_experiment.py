# This script generates all of the data for the "worst practices" experiment
# in the paper. Run it while in the `hip_plugin_framework` directory, then copy
# the .json files from `hip_plugin_framework/results/`.
import argparse
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
    to_return = []

    # We'll also copy and modify this top-level config, generally only to
    # change the scenario name.
    overall_config = {
        "name": "MM1024 vs MM1024",
        "max_iterations": 0,
        "max_time": 10.0,
        "gpu_device_id": 0,
        "pin_cpus": True,
        "do_warmup": True,
        "omit_block_times": True,
        "sync_every_iteration": False,
        "plugins": [mm1024_config]
    }

    # 1024: isolated
    mm1024_config["label"] = "Isolated"
    mm1024_config["log_name"] = "./results/1024_isolated.json"
    overall_config["name"] = "MM1024 Isolated"
    overall_config["plugins"] = [mm1024_config]
    to_return.append(json.dumps(overall_config))

    # 256: isolated
    mm256_config["label"] = "Isolated"
    mm256_config["log_name"] = "./results/256_isolated.json"
    overall_config["name"] = "MM256 Isolated"
    overall_config["plugins"] = [mm256_config]
    to_return.append(json.dumps(overall_config))

    overall_config["name"] = "MM1024 vs MM1024"
    # 1024 vs 1024: Fully shared GPU
    mm1024_config["label"] = "Full GPU Sharing"
    mm1024_config["log_name"] = "./results/1024_vs_1024_full_shared.json"
    competitor1024 = copy.deepcopy(mm1024_config)
    competitor1024["log_name"] = "/dev/null"
    competitor1024["label"] = "Competitor"
    overall_config["plugins"] = [mm1024_config, competitor1024]
    to_return.append(json.dumps(overall_config))
    # Partitioned equally
    mm1024_config["label"] = "Evenly Partitioned"
    mm1024_config["log_name"] = "./results/1024_vs_1024_evenly_partitioned.json"
    mm1024_config["compute_unit_mask"] = "10" * 30
    competitor1024["compute_unit_mask"] = "01" * 30
    to_return.append(json.dumps(overall_config))
    # Uneven partitioned
    mm1024_config["label"] = "Partitioned, w/ Additional Shared CU"
    mm1024_config["log_name"] = "./results/1024_vs_1024_unevenly_partioned.json"
    mm1024_config["compute_unit_mask"] = "10" * 29 + "11"
    to_return.append(json.dumps(overall_config))

    # Remove the CU masks
    del mm1024_config["compute_unit_mask"]
    del competitor1024["compute_unit_mask"]

    overall_config["name"] = "MM1024 vs MM256"
    # 1024 vs 256: Fully shared GPU
    mm1024_config["log_name"] = "./results/1024_vs_256_full_shared.json"
    mm1024_config["label"] = "Full GPU Sharing"
    competitor256 = copy.deepcopy(mm256_config)
    competitor256["log_name"] = "/dev/null"
    competitor256["label"] = "Competitor"
    overall_config["plugins"] = [mm1024_config, competitor256]
    to_return.append(json.dumps(overall_config))
    # Partitioned equally
    mm1024_config["log_name"] = "./results/1024_vs_256_evenly_partitioned.json"
    mm1024_config["label"] = "Evenly Partitioned"
    mm1024_config["compute_unit_mask"] = "10" * 30
    competitor256["compute_unit_mask"] = "01" * 30
    to_return.append(json.dumps(overall_config))
    # Uneven partitioned
    mm1024_config["log_name"] = "./results/1024_vs_256_unevenly_partitioned.json"
    mm1024_config["label"] = "Partitioned, w/ Additional Shared CU"
    mm1024_config["compute_unit_mask"] = "10" * 29 + "11"
    to_return.append(json.dumps(overall_config))

    # Remove CU masks again
    del mm1024_config["compute_unit_mask"]
    del competitor256["compute_unit_mask"]

    overall_config["name"] = "MM256 vs MM256"
    # 256 vs 256: Fully shared GPU
    mm256_config["log_name"] = "./results/256_vs_256_full_shared.json"
    mm256_config["label"] = "Full GPU Sharing"
    overall_config["plugins"] = [mm256_config, competitor256]
    to_return.append(json.dumps(overall_config))
    # Partitioned equally
    mm256_config["log_name"] = "./results/256_vs_256_evenly_partitioned.json"
    mm256_config["label"] = "Evenly Partitioned"
    mm256_config["compute_unit_mask"] = "10" * 30
    competitor256["compute_unit_mask"] = "01" * 30
    to_return.append(json.dumps(overall_config))
    # Uneven partitioned
    mm256_config["log_name"] = "./results/256_vs_256_unevenly_partitioned.json"
    mm256_config["label"] = "Partitioned, w/ Additional Shared CU"
    mm256_config["compute_unit_mask"] = "10" * 29 + "11"
    to_return.append(json.dumps(overall_config))

    # Remove CU masks again
    del mm256_config["compute_unit_mask"]
    del competitor256["compute_unit_mask"]

    overall_config["name"] = "MM256 vs MM1024"
    # 256 vs 1024: Fully shared GPU
    mm256_config["log_name"] = "./results/256_vs_1024_full_shared.json"
    mm256_config["label"] = "Full GPU Sharing"
    overall_config["plugins"] = [mm256_config, competitor1024]
    to_return.append(json.dumps(overall_config))
    # Partitioned equally
    mm256_config["log_name"] = "./results/256_vs_1024_evenly_partitioned.json"
    mm256_config["label"] = "Evenly Partitioned"
    mm256_config["compute_unit_mask"] = "10" * 30
    competitor1024["compute_unit_mask"] = "01" * 30
    to_return.append(json.dumps(overall_config))
    # Uneven partitioned
    mm256_config["log_name"] = "./results/256_vs_1024_unevenly_partitioned.json"
    mm256_config["label"] = "Partitioned, w/ Additional Shared CU"
    mm256_config["compute_unit_mask"] = "10" * 29 + "11"
    to_return.append(json.dumps(overall_config))

    # All done
    return to_return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_experiment", type=int, default=1,
        help="The number of the first experiment to resume from, for use if "+
            "one of the tests hangs.")
    args = parser.parse_args()
    configs = generate_configs()
    for i in range(args.start_experiment - 1, len(configs)):
        print("Running experiment %d of %d" % (i + 1, len(configs)))
        config = configs[i]
        process = subprocess.Popen(["./bin/runner", "-"],
            stdin=subprocess.PIPE)
        process.communicate(input=config)
        print("Sleeping a bit.\n")
        time.sleep(2.0)

