import time
import datetime
import memory_profiler as mem_profile
import cProfile
import pstats

from functools import wraps

import sys
import threading

try:
    import thread
except ImportError:
    import _thread as thread


def exit_after(s):
    def quit_function(fn_name):
        sys.stderr.flush()
        thread.interrupt_main()  # raises KeyboardInterrupt

    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result

        return inner

    return outer


def timer(prec_or_func=None):
    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "prec_or_func" not in locals() or callable(prec_or_func) or prec_or_func is None:
                prec = 5
            else:
                prec = prec_or_func

            start = time.perf_counter()
            val = func(*args, **kwargs)
            print(f"Execution time : {(time.perf_counter() - start):.{prec}f} seconds")

            return val

        return wrapper

    return _decorator(prec_or_func) if callable(prec_or_func) else _decorator


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with open("logs.txt", "a") as f:
            state = "function" if func.__name__ == func.__qualname__ else "method"
            f.write(
                f'Called {state} "{func.__name__}" with args: {args if state == "function" else args[1:]} and kwargs: {kwargs} at {datetime.datetime.today()}.\n'
            )
        val = func(*args, **kwargs)
        return val

    return wrapper


def memory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Running function "{func.__name__}"')
        v1 = mem_profile.memory_usage()
        print(f"Memory (before) : {float(v1[0])} Mb")

        val = func(*args, **kwargs)

        v2 = mem_profile.memory_usage()
        print(f"Memory (after) : {float(v2[0])} Mb")
        print(f"Total memory usage : {float(v2[0]) - float(v1[0])} Mb\n")
        return val

    return wrapper


def profiler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            val = func(*args, **kwargs)
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()

        return val

    return wrapper


"""
def decorator_name(any_number_of_arguments):
	def pseudo_decorator(function_to_be_decorated):
		@wraps(function_to_be_decorated)
		def real_wrapper(*args, **kwargs):

			result = function_to_be_decorated(*args, **kwargs)
			
			return result

		return real_wrapper
	return pseudo_decorator
"""
