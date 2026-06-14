import gc
import math
import statistics
import threading
import timeit

from regions import Cown, Region


def do_work():
    """Do some CPU-intensive work."""
    WORK = 1200_000
    res = 0
    for i in range(WORK):
        res += math.sqrt(i)


def build_large_region():
    OBJS = 2000_000
    region = Region()
    region.l = [[{} for _ in range(OBJS)]]
    return region


def run_experiment(region):
    """Do work and collect a region in parallel."""
    t = threading.Thread(target=do_work)
    t.start()
    gc.collect_region(region)
    t.join()


def benchmark(func):
    results = timeit.repeat(func, repeat=10, number=1)
    mean = round(1000 * statistics.mean(results))
    stdev = round(1000 * statistics.stdev(results))
    return f"{mean} +- {stdev} ms"


cown = Cown(build_large_region())
print("Work, -:", benchmark(lambda: do_work()))
# The region is closed, so the GC releases the GIL.
print("Collect, closed:", benchmark(lambda: gc.collect_region(cown)))
print("Both, closed:", benchmark(lambda: run_experiment(cown)))
# The region is open, so the GC does not release the GIL.
r = cown.value
print("Collect, open:", benchmark(lambda: gc.collect_region(r)))
print("Both, open:", benchmark(lambda: run_experiment(r)))
