import json
from datetime import datetime
from pathlib import Path

from agent.system_result import SystemInfo
from agent.tests.burnin_result import BurnInResult
from agent.tests.test_result import TestResult


class JsonRepository:
    def __init__(self, base_path="data/burnin_runs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, result: BurnInResult):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        machine_id = result.system.machine_id.replace(":", "-")

        filename = f"{timestamp}_{machine_id}.json"
        filepath = self.base_path / filename

        data = {
            "status": result.status,
            "machine": {
                "machine_id": result.system.machine_id,
                "mac_address": result.system.mac_address,
                "hostname": result.system.hostname,
                "operating_system": result.system.operating_system,
                "os_version": result.system.os_version,
                "cpu": result.system.cpu,
                "cpu_count": result.system.cpu_count,
                "ram_total_gb": result.system.ram_total_gb,
            },
            "tests": [
                {
                    "test": test.test,
                    "status": test.status,
                    "errors": test.errors,
                    "metrics": test.metrics,
                }
                for test in result.tests
            ],
        }

        with filepath.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return filepath

    def _from_dict(self, data):
        system = SystemInfo(
            machine_id=data["machine"]["machine_id"],
            mac_address=data["machine"]["mac_address"],
            hostname=data["machine"]["hostname"],
            operating_system=data["machine"]["operating_system"],
            os_version=data["machine"]["os_version"],
            cpu=data["machine"]["cpu"],
            cpu_count=data["machine"]["cpu_count"],
            ram_total_gb=data["machine"]["ram_total_gb"],
        )

        tests = [
            TestResult(
                test=test["test"],
                status=test["status"],
                errors=test.get("errors", []),
                metrics=test.get("metrics", {}),
            )
            for test in data["tests"]
        ]

        return BurnInResult(
            status=data["status"],
            system=system,
            tests=tests,
        )

    def get_history(self, machine_id):
        machine_id = machine_id.replace(":", "-")

        history = []

        for filepath in sorted(
            self.base_path.glob(f"*_{machine_id}.json")
        ):
            with filepath.open("r", encoding="utf-8") as file:
                data = json.load(file)

            history.append(
                self._from_dict(data)
            )

        return history