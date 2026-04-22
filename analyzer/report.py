"""Report builder for downloadable analysis summaries."""

from __future__ import annotations

from analyzer.benchmark import BenchmarkResult
from analyzer.optimize import OptimizationReport
from analyzer.rewrite import RewriteResult
from analyzer.static_analysis import StaticAnalysisResult


def build_report_text(
    code: str,
    static_result: StaticAnalysisResult,
    benchmark_result: BenchmarkResult,
    optimization_report: OptimizationReport,
    rewrite_result: RewriteResult,
    gemini_text: str,
) -> str:
    """Build a plain-text report with all key outputs."""
    lines = [
        "PYTHON COMPLEXITY COACH REPORT",
        "=" * 40,
        "",
        "Original Code:",
        code,
        "",
        "Static Complexity:",
        f"- Time: {static_result.time_complexity}",
        f"- Space: {static_result.space_complexity}",
        f"- Explanation: {static_result.explanation}",
        "",
        "Benchmark Summary:",
        f"- Runtime ms (min/avg/max): {benchmark_result.runtime_min_ms:.3f} / {benchmark_result.runtime_avg_ms:.3f} / {benchmark_result.runtime_max_ms:.3f}",
        f"- Memory KB (min/avg/max): {benchmark_result.memory_min_kb:.3f} / {benchmark_result.memory_avg_kb:.3f} / {benchmark_result.memory_max_kb:.3f}",
        "",
        f"Optimization Score: {optimization_report.score}/100",
        f"Rationale: {optimization_report.rationale}",
        "Suggestions:",
    ]
    lines.extend([f"- {s}" for s in optimization_report.suggestions])
    lines.extend(["", "Interview Feedback:"])
    lines.extend([f"- {s}" for s in optimization_report.interview_feedback])
    lines.extend(["", "Optimized Code:", rewrite_result.optimized_code, "", "Rewrite Explanation:"])
    lines.extend([f"- {item}" for item in rewrite_result.explanation])
    if gemini_text:
        lines.extend(["", "Gemini Insights:", gemini_text])
    return "\n".join(lines)
