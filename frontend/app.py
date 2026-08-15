import streamlit as st

from agent.burnin import run_burnin
from agent.system_info import get_system_info
from agent.storage.json_repository import JsonRepository


st.set_page_config(
    page_title="Burn-in Agent",
    page_icon="🔥",
    layout="wide",
)


def status_color(status):
    if status == "PASS":
        return "🟢"
    return "🔴"


def show_system_info():
    system = get_system_info()

    st.header("Identificação da máquina")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Machine ID",
            system.machine_id,
        )

    with col2:
        st.metric(
            "Processador",
            system.cpu,
        )

    with col3:
        st.metric(
            "Memória RAM",
            f"{system.ram_total_gb:.2f} GB",
        )

    with col4:
        st.metric(
            "CPUs",
            system.cpu_count,
        )

    st.caption(
        f"Hostname: {system.hostname}  |  "
        f"Sistema: {system.operating_system} "
        f"{system.os_version}"
    )


def get_test(result, name):
    return next(
        test
        for test in result.tests
        if test.test == name
    )


def show_result(result):
    st.header("Resultado do Burn-in")

    cpu = get_test(result, "CPU")
    ram = get_test(result, "RAM")

    if result.status == "PASS":
        st.success(
            "🟢 MÁQUINA APROVADA",
            icon="✅",
        )
    else:
        st.error(
            "🔴 MÁQUINA REPROVADA",
            icon="❌",
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "CPU",
            cpu.status,
            delta="Aprovado" if cpu.status == "PASS" else "Falha",
        )

    with col2:
        st.metric(
            "RAM",
            ram.status,
            delta="Aprovado" if ram.status == "PASS" else "Falha",
        )

    with col3:
        st.metric(
            "Resultado Geral",
            result.status,
            delta="APROVADA" if result.status == "PASS" else "REPROVADA",
        )

    st.divider()

    st.subheader("Métricas dos testes")

    cpu_metrics = cpu.metrics
    ram_metrics = ram.metrics

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "CPU média",
            f"{cpu_metrics.get('cpu_average', 0):.1f}%",
        )

    with col2:
        st.metric(
            "CPU máxima",
            f"{cpu_metrics.get('cpu_max', 0):.1f}%",
        )

    with col3:
        st.metric(
            "RAM inicial",
            f"{cpu_metrics.get('ram_initial', 0):.1f}%",
        )

    with col4:
        st.metric(
            "RAM final",
            f"{cpu_metrics.get('ram_final', 0):.1f}%",
        )

    with col5:
        st.metric(
            "RAM máxima",
            f"{ram_metrics.get('ram_max', 0):.1f}%",
        )

    errors = []

    for test in result.tests:
        for error in test.errors:
            errors.append(
                f"{test.test}: {error}"
            )

    if errors:
        st.divider()
        st.subheader("Erros encontrados")

        for error in errors:
            st.error(error)


def show_history():
    system = get_system_info()
    repository = JsonRepository()

    history = repository.get_history(
        system.machine_id
    )

    st.header("Histórico da máquina")

    if not history:
        st.info(
            "Nenhuma execução registrada para esta máquina."
        )
        return

    total = len(history)
    passed = sum(
        1 for result in history
        if result.status == "PASS"
    )
    failed = total - passed

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Execuções",
            total,
        )

    with col2:
        st.metric(
            "Aprovadas",
            passed,
        )

    with col3:
        st.metric(
            "Reprovadas",
            failed,
        )

    st.divider()

    rows = []

    for result in reversed(history):
        cpu = get_test(result, "CPU")
        ram = get_test(result, "RAM")

        rows.append(
            {
                "Resultado": (
                    f"{status_color(result.status)} "
                    f"{result.status}"
                ),
                "CPU": (
                    f"{status_color(cpu.status)} "
                    f"{cpu.status}"
                ),
                "RAM": (
                    f"{status_color(ram.status)} "
                    f"{ram.status}"
                ),
                "CPU média": (
                    f"{cpu.metrics.get('cpu_average', 0):.1f}%"
                ),
                "CPU máxima": (
                    f"{cpu.metrics.get('cpu_max', 0):.1f}%"
                ),
                "RAM máxima": (
                    f"{ram.metrics.get('ram_max', 0):.1f}%"
                ),
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
    )


def main():

    st.title("🔥 Burn-in Agent")

    st.caption(
        "Sistema de teste e validação de máquinas"
    )

    st.divider()

    show_system_info()

    st.divider()

    st.header("Executar teste")

    st.write(
        "Execute o processo de Burn-in para validar "
        "CPU e memória RAM desta máquina."
    )

    if st.button(
        "▶ INICIAR BURN-IN",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner(
            "Executando testes de CPU e RAM..."
        ):
            result = run_burnin()

        st.session_state["last_result"] = result

        st.success(
            "Teste concluído com sucesso."
        )

    if "last_result" in st.session_state:
        st.divider()
        show_result(
            st.session_state["last_result"]
        )

    st.divider()

    show_history()


if __name__ == "__main__":
    main()