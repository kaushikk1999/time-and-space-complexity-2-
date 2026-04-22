"""Streamlit app for Python complexity and performance analysis."""

from __future__ import annotations

import json
from dataclasses import asdict

import streamlit as st

from analyzer.static_analysis import StaticAnalysisResult, analyze_code_complexity
from analyzer.benchmark import BenchmarkResult, benchmark_code
from analyzer.optimize import OptimizationReport, score_and_suggest
from analyzer.rewrite import RewriteResult, rewrite_code
from analyzer.visualize import memory_chart, runtime_chart
from analyzer.report import build_report_text
from analyzer.gemini import gemini_available, get_gemini_insights

st.set_page_config(
    page_title="Python Complexity Coach",
    page_icon="📊",
    layout="wide",
)

SAMPLE_CODE = '''
def contains_duplicates(nums):
    duplicates = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                duplicates.append(nums[i])
    return duplicates

if __name__ == "__main__":
    nums = [1, 2, 3, 2, 4, 5, 1]
    print(contains_duplicates(nums))
'''


def summary_cards(static_result: StaticAnalysisResult, bench_result: BenchmarkResult, score: OptimizationReport) -> None:
    """Render summary metrics."""
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Estimated Time Complexity", static_result.time_complexity)
    c2.metric("Estimated Space Complexity", static_result.space_complexity)
    c3.metric("Avg Runtime (ms)", f"{bench_result.runtime_avg_ms:.3f}")
    c4.metric("Optimization Score", f"{score.score}/100")


def main() -> None:
    """Main Streamlit entry point."""
    st.title("📊 Python Time & Space Complexity Coach")
    st.write(
        "Paste Python code to estimate complexity, benchmark runtime/memory, "
        "get optimization suggestions, and receive interview-style feedback."
    )

    with st.sidebar:
        st.header("Controls")
        iterations = st.slider("Benchmark iterations", min_value=3, max_value=50, value=10)
        api_key = st.text_input("Gemini API Key (optional)", type="password")
        use_example = st.button("Load sample code")

    if "code_input" not in st.session_state:
        st.session_state.code_input = ""

    if use_example:
        st.session_state.code_input = SAMPLE_CODE

    code = st.text_area(
        "Python code",
        value=st.session_state.code_input,
        height=320,
        help="Include a function and optional __main__ block. Avoid external dependencies.",
    )

    analyze_btn = st.button("Analyze & Optimize", type="primary", use_container_width=True)

    if analyze_btn:
        if not code.strip():
            st.error("Please provide Python code first.")
            st.stop()

        with st.spinner("Running static analysis and profiling..."):
            try:
                static_result = analyze_code_complexity(code)
                bench_result = benchmark_code(code, iterations=iterations)
                opt_report = score_and_suggest(static_result, bench_result)
                rewrite_result = rewrite_code(code, static_result, opt_report)
            except Exception as exc:  # noqa: BLE001
                st.exception(exc)
                st.stop()

        summary_cards(static_result, bench_result, opt_report)

        st.subheader("Complexity Explanation")
        st.markdown(static_result.explanation)

        st.subheader("Performance Charts")
        rc1, rc2 = st.columns(2)
        with rc1:
            st.plotly_chart(runtime_chart(bench_result.runtime_ms), use_container_width=True)
        with rc2:
            st.plotly_chart(memory_chart(bench_result.memory_kb), use_container_width=True)

        st.subheader("Optimization Suggestions")
        for idx, suggestion in enumerate(opt_report.suggestions, start=1):
            st.markdown(f"**{idx}.** {suggestion}")

        st.subheader("Interview Feedback")
        for idx, item in enumerate(opt_report.interview_feedback, start=1):
            st.markdown(f"- {item}")

        st.subheader("Code Rewrite (Original vs Optimized)")
        cc1, cc2 = st.columns(2)
        with cc1:
            st.caption("Original")
            st.code(code, language="python")
        with cc2:
            st.caption("Optimized")
            st.code(rewrite_result.optimized_code, language="python")
            st.markdown("**Rewrite rationale**")
            for line in rewrite_result.explanation:
                st.markdown(f"- {line}")

        gemini_text = ""
        st.subheader("Optional Enhanced Insights")
        if gemini_available(api_key):
            gemini_text = get_gemini_insights(
                api_key=api_key,
                code=code,
                static_result=static_result,
                benchmark_result=bench_result,
                optimization_report=opt_report,
            )
            st.markdown(gemini_text)
        else:
            st.info("Gemini key not provided or client unavailable. Core insights shown above are deterministic.")

        report_text = build_report_text(
            code=code,
            static_result=static_result,
            benchmark_result=bench_result,
            optimization_report=opt_report,
            rewrite_result=rewrite_result,
            gemini_text=gemini_text,
        )

        st.download_button(
            "Download analysis report (.txt)",
            data=report_text,
            file_name="complexity_report.txt",
            mime="text/plain",
        )

        st.download_button(
            "Download structured JSON",
            data=json.dumps(
                {
                    "static": asdict(static_result),
                    "benchmark": asdict(bench_result),
                    "optimization": asdict(opt_report),
                    "rewrite": asdict(rewrite_result),
                    "gemini": gemini_text,
                },
                indent=2,
            ),
            file_name="complexity_report.json",
            mime="application/json",
        )

    st.markdown("---")
    st.caption(
        "Limitations: complexity is heuristic, benchmark execution is sandboxed with restricted builtins, "
        "and results can vary by machine load."
    )


if __name__ == "__main__":
    main()
