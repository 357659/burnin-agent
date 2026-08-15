from dataclasses import dataclass


@dataclass
class SystemInfo:
    machine_id: str
    mac_address: str
    hostname: str
    operating_system: str
    os_version: str
    cpu: str
    cpu_count: int
    ram_total_gb: float