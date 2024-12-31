import platform
import resource
import sys


def set_memory_limit(nr: float):
    if platform.system() != "Linux":
        raise RuntimeError("Currently only Linux is supported.")

    as_percentage = False
    if isinstance(nr, str):
        if nr.endswith("%"):
            nr = float(nr.replace("%", "")) / 100
            if not 0 < nr < 1:
                raise ValueError("Percentage should be between 0 and 100")
            as_percentage = True
        elif nr.endswith("TB"):
            nr = float(nr.replace("TB", "")) * 1024**4
        elif nr.endswith("GB"):
            nr = float(nr.replace("GB", "")) * 1024**3
        elif nr.endswith("MB"):
            nr = float(nr.replace("MB", "")) * 1024**2
        elif nr.endswith("KB"):
            nr = float(nr.replace("KB", "")) * 1024
        elif nr.endswith("B"):
            nr = float(nr.replace("B", ""))

    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    if as_percentage:
        resource.setrlimit(resource.RLIMIT_AS, (int(get_memory() * 1024 * nr), hard))
    else:
        resource.setrlimit(resource.RLIMIT_AS, (int(nr), hard))


def get_memory():
    with open("/proc/meminfo", "r") as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ("MemTotal:"):
                free_memory += int(sline[1])
    return free_memory


def limit_memory(nr):
    def decorator(function):
        def wrapper(*args, **kwargs):
            set_memory_limit(nr)
            try:
                return function(*args, **kwargs)
            except MemoryError:
                mem = get_memory() / 1024**2
                mem_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2
                raise MemoryError(
                    f"Memory Exception: {mem_used:2f} GB used, {mem:2f} GB remain."
                )
                sys.exit(1)

        return wrapper

    return decorator
