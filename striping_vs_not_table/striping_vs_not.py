# This is a quick script that runs four scenarios with different CU masks of
# MM1024 vs MM256.
import argparse
import copy
import json
import subprocess
import time

def generate_configs():
    """ Returns a list of JSON configs, each of which must be run to generate
    the data. """
    # Base configs for MM1024 and MM256
    mm1024_config = {
        "label": "MM1024",
        "filename": "./bin/matrix_multiply.so",
        "log_name": "./results/mm1024_unstriped_even.json",
        "thread_count": 1024,
        "block_count": 1,
        "compute_unit_mask": "0" * 30 + "1" * 30,
        "additional_info": {
            "matrix_width": 1024,
            "skip_copy": True
        }
    }
    mm256_config = {
        "label": "MM256",
        "filename": "./bin/matrix_multiply.so",
        "log_name": "/dev/null",
        "thread_count": 256,
        "block_count": 1,
        "compute_unit_mask": "1" * 30 + "0" * 30,
        "additional_info": {
            "matrix_width": 1024,
            "skip_copy": True
        }
    }

    to_return = []
    # The first overall config: Un-striped even CU masks
    overall_config = {
        "name": "MM1024 vs MM256 (Unstriped Even Partitions)",
        "max_iterations": 0,
        "max_time": 60.0,
        "gpu_device_id": 0,
        "pin_cpus": True,
        "do_warmup": True,
        "omit_block_times": True,
        "sync_every_iteration": False,
        "plugins": [mm1024_config, mm256_config]
    }
    to_return.append(json.dumps(overall_config))

    # Second experiment: Un-striped uneven CU masks
    overall_config["name"] = "MM1024 vs MM256 (Unstriped Uneven Partitions)"
    mm1024_config["compute_unit_mask"] = "0" * 29 + "1" * 31
    mm1024_config["log_name"] = "./results/mm1024_unstriped_uneven.json",
    to_return.append(json.dumps(overall_config))

    # We already have data for striped even and striped uneven.

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

