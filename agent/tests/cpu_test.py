import time
import multiprocessing
import psutil


def cpu_worker():
    """Mantém um núcleo da CPU ocupado."""
    while True:
        pass


def run_cpu_test(duration=60):
    """
    Executa um teste simples de carga da CPU.

    Args:
        duration: duração do teste em segundos.

    Returns:
        True quando o teste termina normalmente.
    """

    workers = []

    cpu_count = multiprocessing.cpu_count()

    print("=" * 50)
    print("          BURN-IN CPU TEST")
    print("=" * 50)
    print()
    print(f"CPUs disponíveis : {cpu_count}")
    print(f"Duração do teste : {duration} segundos")
    print()
    print("Iniciando teste...")
    print()

    for _ in range(cpu_count):
        process = multiprocessing.Process(target=cpu_worker)
        process.start()
        workers.append(process)

    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            cpu_usage = psutil.cpu_percent(interval=1)

            elapsed = int(time.time() - start_time)

            print(
                f"Tempo: {elapsed:03d}s | "
                f"CPU: {cpu_usage:5.1f}%"
            )

    finally:
        print()
        print("Encerrando teste...")

        for process in workers:
            process.terminate()
            process.join()

    print("Resultado: PASS")
    return True


if __name__ == "__main__":
    run_cpu_test()