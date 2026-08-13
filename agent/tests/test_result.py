from dataclasses import dataclass, field


@dataclass
class TestResult:
    test: str
    status: str
    errors: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)