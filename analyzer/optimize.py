"""Optimization scoring and recommendation engine."""

from __future__ import annotations

from dataclasses import dataclass

from analyzer.benchmark import BenchmarkResult
from analyzer.static_analysis import StaticAnalysisResult


@dataclass
class OptimizationReport:
    """Optimization score and guidance."""

    score: int
    rationale: str
    suggestions: list[str]
    interview_feedback: list[str]


def score_and_suggest(static_result: StaticAnalysisResult, benchmark_result: BenchmarkResult) -> OptimizationReport:
    """Compute efficiency score and generate actionable suggestions."""
    score = 100
    suggestions: list[str] = []
    interview_feedback: list[str] = []

    if "n^2" in static_result.time_complexity or "n^3" in static_result.time_complexity:
        score -= 25
        suggestions.append("Reduce nested loops by precomputing lookups with a set or dict to approach O(n).")

    if static_result.has_recursion:
        score -= 10
        suggestions.append("Consider iterative dynamic programming or memoization to avoid repeated recursion work.")

    if benchmark_result.runtime_avg_ms > 50:
        score -= 20
        suggestions.append("Average runtime is high; cache repeated calculations and avoid redundant passes over data.")

    if benchmark_result.memory_avg_kb > 512:
        score -= 20
        suggestions.append("Memory usage is elevated; prefer generators and in-place updates over building full intermediate lists.")

    if static_result.uses_heavy_structures:
        suggestions.append("Using sets/dicts is often good for speed; ensure the extra memory is justified by faster lookups.")

    if not suggestions:
        suggestions.append("Code is already efficient for this heuristic profile; focus on clarity and edge-case handling.")

    interview_feedback.extend(
        [
            "Explain trade-offs explicitly: readability vs. asymptotic gains.",
            "State assumptions about input size and data distribution during interviews.",
            "Mention Python-specific optimizations (comprehensions, built-ins, hashing) when relevant.",
        ]
    )

    score = max(0, min(100, score))
    rationale = (
        f"Score derived from complexity estimate ({static_result.time_complexity}, {static_result.space_complexity}) "
        f"and empirical profile (avg runtime {benchmark_result.runtime_avg_ms:.2f} ms, "
        f"avg peak memory {benchmark_result.memory_avg_kb:.2f} KB)."
    )

    return OptimizationReport(score=score, rationale=rationale, suggestions=suggestions, interview_feedback=interview_feedback)
