import platform
import psutil

from agent.hardware.disk import get_disks


def get_mac_address():
    interfaces = psutil.net_if_addrs()

    for interface_name, addresses in interfaces.items():
        interface_lower = interface_name.lower()

        # Ignora interfaces virtuais e loopback
        if (
            "loopback" in interface_lower
            or "virtual" in interface_lower
            or "vethernet" in interface_lower
            or "docker" in interface_lower
        ):
            continue

        for address in addresses:
            # Família -1 = endereço MAC no Windows
            if address.family == -1:
                return address.address.replace("-", ":").upper()

    return "N/A"


def get_cpu_info():
    return platform.processor()


def get_memory_info():
    memory = psutil.virtual_memory()
    return memory.total


def format_bytes(value):
    gb = value / (1024 ** 3)
    return f"{gb:.2f} GB"


def get_network_interfaces():
    interfaces = psutil.net_if_addrs()

    for interface_name, addresses in interfaces.items():
        print(f"\nInterface: {interface_name}")

        for address in addresses:
            print(f"  Família : {address.family}")
            print(f"  Endereço: {address.address}")


def show_storage():
    disks = get_disks()

    for index, disk in enumerate(disks, start=1):
        print(f"Disco {index}")
        print(f"  Modelo    : {disk['model']}")
        print(f"  Serial    : {disk['serial']}")
        print(f"  Capacidade: {disk['size_gb']} GB")
        print(f"  Interface : {disk['interface']}")
        print()


def main():
    print("=" * 50)
    print("              BURN-IN AGENT v0.2")
    print("=" * 50)
    print()

    print("EQUIPAMENTO")
    print("-" * 50)

    print(f"MAC Ethernet : {get_mac_address()}")
    print(f"CPU          : {get_cpu_info()}")
    print(f"RAM          : {format_bytes(get_memory_info())}")

    print()
    print("INTERFACES DE REDE")
    print("-" * 50)

    get_network_interfaces()

    print()
    print("ARMAZENAMENTO")
    print("-" * 50)

    show_storage()

    print("-" * 50)
    print("Status: READY")
    print("-" * 50)


if __name__ == "__main__":
    main()