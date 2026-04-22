"""Runtime and memory benchmarking in a constrained execution environment."""

from __future__ import annotations

import statistics
import time
import tracemalloc
from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    """Runtime and memory benchmark outputs."""

    runtime_ms: list[float]
    memory_kb: list[float]
    runtime_min_ms: float
    runtime_avg_ms: float
    runtime_max_ms: float
    memory_min_kb: float
    memory_avg_kb: float
    memory_max_kb: float


SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "print": print,
    "range": range,
    "set": set,
    "sorted": sorted,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}


def _execute(code: str) -> None:
    """Execute user code with restricted builtins."""
    namespace: dict[str, object] = {"__builtins__": SAFE_BUILTINS, "__name__": "__main__"}
    compiled = compile(code, "<user_code>", "exec")
    exec(compiled, namespace, namespace)  # noqa: S102


def benchmark_code(code: str, iterations: int = 10) -> BenchmarkResult:
    """Measure runtime and peak memory across repeated isolated executions."""
    runtime_ms: list[float] = []
    memory_kb: list[float] = []

    for _ in range(iterations):
        tracemalloc.start()
        start = time.perf_counter()
        _execute(code)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        runtime_ms.append(elapsed_ms)
        memory_kb.append(peak / 1024.0)

    return BenchmarkResult(
        runtime_ms=runtime_ms,
        memory_kb=memory_kb,
        runtime_min_ms=min(runtime_ms),
        runtime_avg_ms=statistics.mean(runtime_ms),
        runtime_max_ms=max(runtime_ms),
        memory_min_kb=min(memory_kb),
        memory_avg_kb=statistics.mean(memory_kb),
        memory_max_kb=max(memory_kb),
    )
