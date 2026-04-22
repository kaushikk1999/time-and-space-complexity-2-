"""Simple deterministic code rewrite heuristics."""

from __future__ import annotations

from dataclasses import dataclass

from analyzer.optimize import OptimizationReport
from analyzer.static_analysis import StaticAnalysisResult


@dataclass
class RewriteResult:
    """Optimized code proposal and explanation."""

    optimized_code: str
    explanation: list[str]


def rewrite_code(code: str, static_result: StaticAnalysisResult, optimization_report: OptimizationReport) -> RewriteResult:
    """Produce a practical rewritten candidate with deterministic rules."""
    explanation: list[str] = []
    optimized_code = code

    if static_result.loop_depth >= 2 and "for j in range(i + 1" in code and "duplicates" in code:
        optimized_code = '''
def contains_duplicates(nums):
    seen = set()
    dupes = set()
    for value in nums:
        if value in seen:
            dupes.add(value)
        else:
            seen.add(value)
    return sorted(dupes)

if __name__ == "__main__":
    nums = [1, 2, 3, 2, 4, 5, 1]
    print(contains_duplicates(nums))
'''
        explanation.extend(
            [
                "Replaced nested index comparison with one linear pass using hash sets.",
                "Reduced time complexity from O(n^2) to O(n) average-case.",
                "Used set membership checks for constant-time duplicate detection.",
            ]
        )
    else:
        explanation.extend(
            [
                "No strong deterministic rewrite pattern matched the input.",
                "Retained original code and surfaced optimization suggestions for manual refactor.",
            ]
        )

    if optimization_report.score < 70:
        explanation.append("Priority: focus on removing redundant iterations and intermediate allocations.")

    return RewriteResult(optimized_code=optimized_code, explanation=explanation)
