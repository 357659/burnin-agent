import multiprocessing
import time

import psutil

from agent.tests.result import evaluate_cpu_result
from agent.config.settings import CPU_TEST_DURATION

def cpu_worker():
    """Mantém um núcleo da CPU ocupado."""
    while True:
        pass


def run_cpu_test(duration=CPU_TEST_DURATION):
    """
    Executa um teste de carga da CPU.

    Retorna um dicionário com as métricas coletadas.
    """

    workers = []
    cpu_count = multiprocessing.cpu_count()

    cpu_samples = []
    ram_samples = []

    print("=" * 50)
    print("          BURN-IN CPU TEST")
    print("=" * 50)
    print()
    print(f"CPUs disponíveis : {cpu_count}")
    print(f"Duração do teste : {duration} segundos")
    print()
    print("Iniciando teste...")
    print()

    # Inicia um processo por núcleo lógico
    for _ in range(cpu_count):
        process = multiprocessing.Process(target=cpu_worker)
        process.start()
        workers.append(process)

    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()

            cpu_samples.append(cpu_usage)
            ram_samples.append(memory.percent)

            elapsed = int(time.time() - start_time)

            print(
                f"[{elapsed:03d}s] "
                f"CPU: {cpu_usage:5.1f}% | "
                f"RAM: {memory.percent:5.1f}%"
            )

    finally:
        print()
        print("Encerrando teste...")

        for process in workers:
            process.terminate()
            process.join()

    # Calcula as métricas
    cpu_average = sum(cpu_samples) / len(cpu_samples)
    cpu_max = max(cpu_samples)

    ram_initial = ram_samples[0]
    ram_final = ram_samples[-1]

    result = {
        "duration_seconds": duration,
        "cpu_average": round(cpu_average, 2),
        "cpu_max": round(cpu_max, 2),
        "ram_initial": round(ram_initial, 2),
        "ram_final": round(ram_final, 2),
    }

    # Avalia o resultado
    evaluation = evaluate_cpu_result(
        result["cpu_average"],
        result["cpu_max"],
    )

    print()
    print("=" * 50)
    print("              RESULTADO")
    print("=" * 50)
    print()

    print(f"Duração       : {result['duration_seconds']} s")
    print(f"CPU média     : {result['cpu_average']} %")
    print(f"CPU máxima    : {result['cpu_max']} %")
    print(f"RAM inicial   : {result['ram_initial']} %")
    print(f"RAM final     : {result['ram_final']} %")
    print()

    print(f"Resultado     : {evaluation['status']}")

    if evaluation["errors"]:
        print()
        print("Motivos:")

        for error in evaluation["errors"]:
            print(f"- {error}")

    print("=" * 50)

    return result


if __name__ == "__main__":
    run_cpu_test()  # Executa o teste usando a duração configurada em settings.py