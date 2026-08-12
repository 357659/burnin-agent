import time

from agent.monitor.collector import get_cpu_usage, get_memory_usage


def show_monitoring():
    print("=" * 50)
    print("          BURN-IN AGENT v0.3")
    print("=" * 50)
    print()

    print("MONITORAMENTO EM TEMPO REAL")
    print("-" * 50)

    try:
        while True:
            cpu = get_cpu_usage()
            memory = get_memory_usage()

            print(
                f"\rCPU: {cpu:5.1f}% | "
                f"RAM: {memory['percent']:5.1f}% | "
                f"RAM: {memory['used_gb']:.2f} / "
                f"{memory['total_gb']:.2f} GB",
                end="",
                flush=True,
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n")
        print("Monitoramento encerrado.")


if __name__ == "__main__":
    show_monitoring()