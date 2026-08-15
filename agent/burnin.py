from agent.tests.cpu_test import run_cpu_test
from agent.tests.ram_test import run_ram_test
from agent.system_info import get_system_info
from agent.tests.burnin_result import BurnInResult

def run_burnin():
    system_info = get_system_info()

    print("=" * 50)
    print("             BURN-IN AGENT")
    print("=" * 50)

    print(f"{'ID da Máquina':20}: {system_info.machine_id}")
    print(f"{'Endereço MAC':20}: {system_info.mac_address}")
    print(f"{'Hostname':20}: {system_info.hostname}")
    print(f"{'Sistema Operacional':20}: {system_info.operating_system}")
    print(f"{'Versão do SO':20}: {system_info.os_version}")
    print(f"{'CPU':20}: {system_info.cpu}")
    print(f"{'Quantidade de CPUs':20}: {system_info.cpu_count}")
    print(f"{'Memória RAM Total (GB)':20}: {system_info.ram_total_gb}")

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
        system=system_info,
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