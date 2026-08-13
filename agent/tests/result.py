def evaluate_cpu_result(cpu_average, cpu_max):
    """
    Avalia o resultado do teste de CPU.
    """

    errors = []

    if cpu_average < 90:
        errors.append(
            f"CPU média abaixo do esperado: {cpu_average:.2f}%"
        )

    if cpu_max < 95:
        errors.append(
            f"CPU máxima abaixo do esperado: {cpu_max:.2f}%"
        )

    if errors:
        return {
            "status": "FAIL",
            "errors": errors,
        }

    return {
        "status": "PASS",
        "errors": [],
    }
