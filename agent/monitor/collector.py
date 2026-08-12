import psutil


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()

    return {
        "percent": memory.percent,
        "used_gb": memory.used / (1024 ** 3),
        "total_gb": memory.total / (1024 ** 3),
    }