from agent.config.settings import CPU_MIN_AVERAGE, CPU_MIN_MAX
from agent.tests.test_result import TestResult


def build_test_result(test_name, status, errors, metrics=None):
    return TestResult(
        test=test_name,
        status=status,
        errors=errors,
        metrics=metrics or {},
    )


def evaluate_cpu_result(
    cpu_average,
    cpu_max,
    ram_initial,
    ram_final,
):
    """
    Avalia o resultado do teste de CPU.
    """

    errors = []

    if cpu_average < CPU_MIN_AVERAGE:
        errors.append(
            f"CPU média abaixo do esperado: {cpu_average:.2f}%"
        )

    if cpu_max < CPU_MIN_MAX:
        errors.append(
            f"CPU máxima abaixo do esperado: {cpu_max:.2f}%"
        )

    metrics = {
        "cpu_average": cpu_average,
        "cpu_max": cpu_max,
        "ram_initial": ram_initial,
        "ram_final": ram_final,
    }

    if errors:
        return build_test_result(
            "CPU",
            "FAIL",
            errors,
            metrics,
        )

    return build_test_result(
        "CPU",
        "PASS",
        [],
        metrics,
    )