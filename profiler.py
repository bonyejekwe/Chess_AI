
# profiler.py: A simple profiling class (Professor Rachlin's profiling decorator).

from collections import defaultdict
import time


class Profiler:

    calls = defaultdict(int)  # default 0
    time = defaultdict(float)  # default 0.0

    def __init__(self):
        pass

    @staticmethod
    def add(name, sec):
        Profiler.calls[name] += 1
        Profiler.time[name] += sec

    @staticmethod
    def profile(f):
        def wrapper(*args, **kwargs):
            fname = str(f).split()[1]
            start = time.time_ns()
            val = f(*args, **kwargs)
            sec = (time.time_ns() - start) / 10**9
            Profiler.add(fname, sec)
            return val

        return wrapper

    @staticmethod
    def report():
        print("Function                   Calls     TotSec   Sec/Call")
        for name, num in Profiler.calls.items():
            sec = Profiler.time[name]
            print(f'{name:25s} {num:6d} {sec:10.8f} {sec / num:10.8f}')
