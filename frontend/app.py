import streamlit as st

from agent.burnin import run_burnin
from agent.system_info import get_system_info
from agent.storage.json_repository import JsonRepository


st.set_page_config(
    page_title="Burn-in Agent",
    page_icon="🖥️",
    layout="wide",
)


def show_system_info():
    system = get_system_info()

    st.subheader("Identificação da máquina")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Machine ID", system.machine_id)

    with col2:
        st.metric("CPU", system.cpu)

    with col3:
        st.metric("RAM", f"{system.ram_total_gb:.2f} GB")

    with col4:
        st.metric("CPUs", system.cpu_count)

    st.caption(
        f"Hostname: {system.hostname} | "
        f"Sistema: {system.operating_system} "
        f"{system.os_version}"
    )

    st.divider()

    st.subheader("Armazenamento")

    if not system.disks:
        st.info("Nenhuma unidade de armazenamento encontrada.")
        return

    columns = st.columns(len(system.disks))

    for column, disk in zip(columns, system.disks):
        with column:
            st.metric(
                disk.device,
                f"{disk.total_gb:.2f} GB",
            )

            st.caption(
                f"Livre: {disk.free_gb:.2f} GB | "
                f"{disk.filesystem}"
            )


def show_result(result):
    st.subheader("Resultado do Burn-in")

    col1, col2, col3 = st.columns(3)

    cpu_result = next(
        test for test in result.tests
        if test.test == "CPU"
    )

    ram_result = next(
        test for test in result.tests
        if test.test == "RAM"
    )

    with col1:
        st.metric(
            "CPU",
            cpu_result.status,
        )

    with col2:
        st.metric(
            "RAM",
            ram_result.status,
        )

    with col3:
        st.metric(
            "Resultado Geral",
            result.status,
        )

    st.divider()

    st.write("### Métricas")

    cpu_metrics = cpu_result.metrics
    ram_metrics = ram_result.metrics

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "CPU média",
            f"{cpu_metrics['cpu_average']:.1f}%",
        )

    with col2:
        st.metric(
            "CPU máxima",
            f"{cpu_metrics['cpu_max']:.1f}%",
        )

    with col3:
        st.metric(
            "RAM máxima",
            f"{ram_metrics['ram_max']:.1f}%",
        )

    with col4:
        st.metric(
            "RAM inicial",
            f"{cpu_metrics['ram_initial']:.1f}%",
        )

    if result.status == "PASS":
        st.success("✓ Máquina aprovada no Burn-in.")
    else:
        st.error("✗ Máquina reprovada no Burn-in.")

        for test in result.tests:
            for error in test.errors:
                st.error(f"{test.test}: {error}")


def show_history():
    system = get_system_info()
    repository = JsonRepository()

    history = repository.get_history(system.machine_id)

    st.subheader("Histórico da máquina")

    if not history:
        st.info("Nenhuma execução registrada.")
        return

    rows = []

    for result in history:
        cpu = next(
            test for test in result.tests
            if test.test == "CPU"
        )

        ram = next(
            test for test in result.tests
            if test.test == "RAM"
        )

        rows.append(
            {
                "Resultado": result.status,
                "CPU": cpu.status,
                "RAM": ram.status,
                "CPU média": cpu.metrics.get(
                    "cpu_average",
                    0,
                ),
                "CPU máxima": cpu.metrics.get(
                    "cpu_max",
                    0,
                ),
                "RAM máxima": ram.metrics.get(
                    "ram_max",
                    0,
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

    show_system_info()

    st.divider()

    st.subheader("Executar teste")

    if st.button(
        "▶ INICIAR BURN-IN",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner(
            "Executando testes de CPU e RAM..."
        ):
            result = run_burnin()
        repository = JsonRepository()
        filepath = repository.save(result)

        st.session_state["last_result"] = result

    if "last_result" in st.session_state:
        show_result(
            st.session_state["last_result"]
        )

    st.divider()

    show_history()


if __name__ == "__main__":
    main()