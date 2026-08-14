import time
import psutil

from agent.config.settings import RAM_MAX_USAGE, RAM_TEST_DURATION
from agent.tests.result import build_test_result
from agent.config.settings import (
    RAM_MAX_USAGE,
    RAM_TEST_DURATION,
    RAM_TEST_USAGE,
)
def calculate_memory_to_allocate():
    memory = psutil.virtual_memory()

    target_percent = RAM_TEST_USAGE / 100

    return int(memory.total * target_percent)
def run_ram_test(duration=RAM_TEST_DURATION):
    """
    Monitora o uso da memória RAM durante o teste.
    """

    samples = []

    start_time = time.time()

    while time.time() - start_time < duration:
        memory = psutil.virtual_memory()
        samples.append(memory.percent)

        time.sleep(1)

    ram_max = max(samples)

    errors = []

    if ram_max > RAM_MAX_USAGE:
        errors.append(
            f"Uso máximo de RAM acima do esperado: {ram_max:.2f}%"
        )

    if errors:
        return build_test_result("RAM", "FAIL", errors)

    return build_test_result("RAM", "PASS", [])


if __name__ == "__main__":
    result = run_ram_test()

    print("=" * 50)
    print("              RESULTADO RAM")
    print("=" * 50)

    print(f"RAM máxima    : {max(psutil.virtual_memory().percent, 0):.1f}%")
    print(f"Resultado     : {result.status}")

    if result.errors:
        print("\nMotivos:")
        for error in result.errors:
            print(f"- {error}")

    print("=" * 50)