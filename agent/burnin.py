from agent.tests.cpu_test import run_cpu_test
from agent.tests.ram_test import run_ram_test


def run_burnin():
    print("=" * 50)
    print("             BURN-IN AGENT")
    print("=" * 50)

    print("\nIniciando teste de CPU...")
    cpu_result = run_cpu_test()

    print("\nIniciando teste de RAM...")

    ram_result = run_ram_test()
    

    results = [
        cpu_result,
        ram_result,
    ]

    failed_tests = [
        result
        for result in results
        if result.status == "FAIL"
    ]

    if failed_tests:
        status = "FAIL"
    else:
        status = "PASS"

    print()
    print("=" * 50)
    print("          RESULTADO FINAL")
    print("=" * 50)

    print(f"CPU : {cpu_result.status}")
    print(f"RAM : {ram_result.status}")
    print()
    print(f"RESULTADO GERAL : {status}")
    print("=" * 50)

    return status


if __name__ == "__main__":
    run_burnin()