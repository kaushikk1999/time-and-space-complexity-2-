"""Plotly visualizations for profiling metrics."""

from __future__ import annotations

import plotly.graph_objects as go


def runtime_chart(runtime_ms: list[float]) -> go.Figure:
    """Create runtime line chart."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(runtime_ms) + 1)),
            y=runtime_ms,
            mode="lines+markers",
            name="Runtime (ms)",
        )
    )
    fig.update_layout(title="Runtime per Iteration", xaxis_title="Iteration", yaxis_title="ms")
    return fig


def memory_chart(memory_kb: list[float]) -> go.Figure:
    """Create memory bar chart."""
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=list(range(1, len(memory_kb) + 1)),
            y=memory_kb,
            name="Memory (KB)",
        )
    )
    fig.update_layout(title="Peak Memory per Iteration", xaxis_title="Iteration", yaxis_title="KB")
    return fig
