import time
import psutil

from agent.tests.result import build_test_result
from agent.config.settings import (
    RAM_MAX_USAGE,
    RAM_TEST_DURATION,
    RAM_TEST_USAGE,
    RAM_TEST_MAX_ALLOCATION_MB,
)


def calculate_memory_to_allocate():
    memory = psutil.virtual_memory()

    target_percent = RAM_TEST_USAGE / 100

    target_memory = int(memory.total * target_percent)

    return min(target_memory, memory.available)


def allocate_memory(size_bytes):
    block_size = 1024 * 1024
    blocks = []

    allocated = 0

    while allocated < size_bytes:
        size = min(block_size, size_bytes - allocated)

        block = bytearray(size)

        # Escreve nos bytes para garantir que a memória seja realmente utilizada.
        for i in range(0, size, 4096):
            block[i] = 1

        blocks.append(block)
        allocated += size

    return blocks


def run_ram_test(duration=RAM_TEST_DURATION):
    """
    Executa um teste de carga da memória RAM.
    """

    samples = []

    max_allocation = RAM_TEST_MAX_ALLOCATION_MB * 1024 * 1024

    memory_to_allocate = min(
        calculate_memory_to_allocate(),
        max_allocation,
    )

    print(f"Memória a alocar : {memory_to_allocate / (1024 ** 2):.1f} MB")

    test_memory = allocate_memory(memory_to_allocate)

    start_time = time.time()

    while time.time() - start_time < duration:
        memory = psutil.virtual_memory()

        samples.append(memory.percent)

        elapsed = int(time.time() - start_time)

        print(
            f"[{elapsed:03d}s] "
            f"RAM: {memory.percent:5.1f}%"
        )

        time.sleep(1)

    ram_max = max(samples)

    del test_memory

    errors = []

    if ram_max > RAM_MAX_USAGE:
        errors.append(
            f"Uso máximo de RAM acima do esperado: {ram_max:.2f}%"
        )

    metrics = {
        "ram_max": ram_max,
    }

    if errors:
        return build_test_result(
            "RAM",
            "FAIL",
            errors,
            metrics,
        )

    return build_test_result(
        "RAM",
        "PASS",
        [],
        metrics,
    )


if __name__ == "__main__":
    result = run_ram_test()

    print("=" * 50)
    print("              RESULTADO RAM")
    print("=" * 50)

    print(f"RAM máxima    : {result.metrics['ram_max']:.1f}%")
    print(f"Resultado     : {result.status}")

    if result.errors:
        print("\nMotivos:")

        for error in result.errors:
            print(f"- {error}")

    print("=" * 50)