from dataclasses import dataclass, field

from agent.system_result import SystemInfo
from agent.tests.test_result import TestResult


@dataclass
class BurnInResult:
    status: str
    system: SystemInfo
    tests: list[TestResult] = field(default_factory=list)