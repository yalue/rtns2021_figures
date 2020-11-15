# This script is intended to measure the performance of a task and an identical
# competitor, while only varying HW queue to which the competitor is assigned.
#
# NOTE: I have not been getting particularly good results with this script--
# I am committing it only to serve as reference for later. If it's not changed
# significantly I will probably delete it.
import argparse
import copy
import json
import subprocess
import time

def generate_config(dummy_queues):
    """ Returns a JSON config where a measured task is separated from a
    competitor by an additional dummy_streams instance, which creates the
    specified number of queues. """
    # Don't allow 0 queues, since it won't work with the dummy task. Instead,
    # we'll always create a dummy, and make sure to create plenty of queues to
    # allow possible wrapping around.
    if dummy_queues <= 0:
        print("Not enough queues requested.")
        exit(1)

    log_name = "results/queue_assignment_%d_sep.json" % (dummy_queues,)
#    measured_task_config = {
#        "label": str(dummy_queues),
#        "log_name": log_name,
#        "filename": "./bin/matrix_multiply.so",
#        "initialization_delay": 0.0,
#        "thread_count": 1024,
#        "block_count": 1,
#        "additional_info": {
#            "matrix_width": 1024,
#            "skip_copy": True
#        }
#    }
    measured_task_config = {
        "label": str(dummy_queues),
        "log_name": log_name,
        "filename": "./bin/counter_spin.so",
        "initialization_delay": 0.0,
        "thread_count": 1024,
        "block_count": 1024 * 50,
        "additional_info": 1000
    }
    dummy_config = {
        "filename": "./bin/dummy_streams.so",
        "log_name": "/dev/null",
        "thread_count": 1,
        "block_count": 1,
        "compute_unit_mask": "0xdeadbeef",
        "initialization_delay": 6.0,
        "additional_info": {
            "stream_count": dummy_queues,
            "use_cu_mask": True
        }
    }

    # Remember the initialization order: measured -> dummy -> competitor
    # Give the competitor plenty of initialization delay, to hopefully ensure
    # that the dummy_queues all get time to initialize and warm up.
    competitor_config = copy.deepcopy(measured_task_config)
    competitor_config["log_name"] = "/dev/null"
    competitor_config["initialization_delay"] = 10.0 + (float(dummy_queues) /
        4.0)

    overall_config = {
        "name": "Queue assignment vs. Performance",
        "max_iterations": 1000000,
        "max_time": 5 * 60.0,
        "gpu_device_id": 0,
        "use_processes": True,
        "do_warmup": True,
        "omit_block_times": True,
        "sync_every_iteration": False,
        "plugins": [measured_task_config, dummy_config, competitor_config]
    }
    return json.dumps(overall_config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_count", type=int, default=1,
        help="The number of queues to start the test with.")
    args = parser.parse_args()
    for count in range(args.start_count, 40):
        print("Running test with %d dummy queues." % (count,))
        c = generate_config(count)
        p = subprocess.Popen(["./bin/runner", "-"], stdin=subprocess.PIPE)
        p.communicate(input=c)
        # This seems to help with hangs during load.
        print("Done. Waiting a bit before the next test.\n\n")
        time.sleep(4.0)

