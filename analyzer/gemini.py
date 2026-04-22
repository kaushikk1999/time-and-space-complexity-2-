"""Optional Gemini integration for enhanced natural-language insights."""

from __future__ import annotations

from analyzer.benchmark import BenchmarkResult
from analyzer.optimize import OptimizationReport
from analyzer.static_analysis import StaticAnalysisResult


def gemini_available(api_key: str | None) -> bool:
    """Check whether Gemini can be used."""
    if not api_key:
        return False
    try:
        import google.generativeai as genai  # noqa: F401
    except Exception:  # noqa: BLE001
        return False
    return True


def get_gemini_insights(
    api_key: str,
    code: str,
    static_result: StaticAnalysisResult,
    benchmark_result: BenchmarkResult,
    optimization_report: OptimizationReport,
) -> str:
    """Request optional Gemini commentary while preserving graceful fallback."""
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
You are an interview coach. Analyze this Python code and provide concise interview-ready advice.

Code:
{code}

Static analysis:
- Time complexity: {static_result.time_complexity}
- Space complexity: {static_result.space_complexity}

Empirical profile:
- Avg runtime: {benchmark_result.runtime_avg_ms:.3f} ms
- Avg memory: {benchmark_result.memory_avg_kb:.3f} KB

Current optimization score: {optimization_report.score}/100

Respond with:
1) Top 3 interview talking points
2) Top 3 optimization actions
3) Risks and edge cases to discuss
"""
        response = model.generate_content(prompt)
        return response.text if getattr(response, "text", None) else "Gemini returned no text."
    except Exception as exc:  # noqa: BLE001
        return f"Gemini insights unavailable due to error: {exc}"
