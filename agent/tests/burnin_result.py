from dataclasses import dataclass, field

from agent.tests.test_result import TestResult


@dataclass
class BurnInResult:
    status: str
    tests: list[TestResult] = field(default_factory=list)