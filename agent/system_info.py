import platform
import socket

import psutil

import hashlib

from agent.system_result import SystemInfo,DiskInfo

def build_machine_id(mac_address):
    normalized = mac_address.replace(":", "").replace("-", "").upper()

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()[:16]

def get_cpu_name():
    import winreg

    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        )

        cpu_name, _ = winreg.QueryValueEx(
            key,
            "ProcessorNameString",
        )

        winreg.CloseKey(key)

        return cpu_name.strip()

    except Exception:
        return "CPU desconhecida"

def get_mac_address():
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for interface_name, addresses in interfaces.items():
        if interface_name not in stats:
            continue

        if not stats[interface_name].isup:
            continue

        for address in addresses:
            if address.family == psutil.AF_LINK:
                mac = address.address

                if mac and mac != "00:00:00:00:00:00":
                    return mac.upper()

    return None

def get_disk_info():
    disks = []

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            disks.append(
                DiskInfo(
                    device=partition.device,
                    mountpoint=partition.mountpoint,
                    filesystem=partition.fstype,
                    total_gb=round(
                        usage.total / (1024 ** 3),
                        2,
                    ),
                    free_gb=round(
                        usage.free / (1024 ** 3),
                        2,
                    ),
                )
            )

        except (PermissionError, OSError):
            continue

    return disks

def get_system_info():
    memory = psutil.virtual_memory()
    mac_address = get_mac_address()

    if mac_address is None:
        raise RuntimeError("Não foi possível identificar um endereço MAC.")

    return SystemInfo(
        machine_id=mac_address,
        mac_address=mac_address,
        hostname=socket.gethostname(),
        operating_system=platform.system(),
        os_version=platform.version(),
        cpu=get_cpu_name(),
        cpu_count=psutil.cpu_count(logical=True),
        ram_total_gb=round(memory.total / (1024 ** 3), 2),
        disks=get_disk_info(),
    )


if __name__ == "__main__":
    info = get_system_info()

    print("=" * 50)
    print("             SYSTEM INFO")
    print("=" * 50)

    print(f"{'machine_id':20}: {info.machine_id}")
    print(f"{'mac_address':20}: {info.mac_address}")
    print(f"{'hostname':20}: {info.hostname}")
    print(f"{'operating_system':20}: {info.operating_system}")
    print(f"{'os_version':20}: {info.os_version}")
    print(f"{'cpu':20}: {info.cpu}")
    print(f"{'cpu_count':20}: {info.cpu_count}")
    print(f"{'ram_total_gb':20}: {info.ram_total_gb}")

    print()
    print("ARMAZENAMENTO:")

    for disk in info.disks:
        print(
            f"{disk.device:10} "
            f"{disk.total_gb:.2f} GB total | "
            f"{disk.free_gb:.2f} GB livre | "
            f"{disk.filesystem}"
        )

    print("=" * 50)