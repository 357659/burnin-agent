from dataclasses import dataclass
from typing import List


@dataclass
class DiskInfo:
    device: str
    mountpoint: str
    filesystem: str
    total_gb: float
    free_gb: float


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
    disks: List[DiskInfo]