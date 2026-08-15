from agent.tests.cpu_test import run_cpu_test
from agent.tests.ram_test import run_ram_test
from agent.tests.burnin_result import BurnInResult

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

    status = "FAIL" if any(
        result.status == "FAIL"
        for result in results
    ) else "PASS"

    burnin_result = BurnInResult(
        status=status,
        tests=results,
    )

    print()
    print("=" * 50)
    print("          RESULTADO FINAL")
    print("=" * 50)

    print(f"CPU : {cpu_result.status}")
    print(f"RAM : {ram_result.status}")
    print()
    print(f"RESULTADO GERAL : {burnin_result.status}")
    print("=" * 50)

    return burnin_result


if __name__ == "__main__":
    run_burnin()