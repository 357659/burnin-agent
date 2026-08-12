import subprocess
import json


def get_disks():
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        """
        Get-CimInstance Win32_DiskDrive |
        Select-Object Model, SerialNumber, Size, InterfaceType |
        ConvertTo-Json
        """
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return []

    output = result.stdout.strip()

    if not output:
        return []

    data = json.loads(output)

    if isinstance(data, dict):
        data = [data]

    disks = []

    for disk in data:
        size = disk.get("Size")

        if size:
            size_gb = int(size) / (1024 ** 3)
        else:
            size_gb = 0

        disks.append({
            "model": disk.get("Model"),
            "serial": disk.get("SerialNumber"),
            "size_gb": round(size_gb, 2),
            "interface": disk.get("InterfaceType")
        })

    return disks