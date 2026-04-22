"""Static AST-driven complexity analysis."""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass
class StaticAnalysisResult:
    """Results for static complexity inspection."""

    time_complexity: str
    space_complexity: str
    explanation: str
    loop_depth: int
    has_recursion: bool
    uses_heavy_structures: bool


class ComplexityVisitor(ast.NodeVisitor):
    """Collect structural signals from Python AST."""

    def __init__(self) -> None:
        self.current_loop_depth = 0
        self.max_loop_depth = 0
        self.function_names: set[str] = set()
        self.recursive_calls = 0
        self.list_comp_count = 0
        self.dict_set_usage = 0
        self.total_assignments = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: D401
        self.function_names.add(node.name)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:  # noqa: D401
        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node: ast.While) -> None:  # noqa: D401
        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_Call(self, node: ast.Call) -> None:  # noqa: D401
        if isinstance(node.func, ast.Name) and node.func.id in self.function_names:
            self.recursive_calls += 1
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:  # noqa: D401
        self.list_comp_count += 1
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:  # noqa: D401
        self.dict_set_usage += 1
        self.generic_visit(node)

    def visit_Set(self, node: ast.Set) -> None:  # noqa: D401
        self.dict_set_usage += 1
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:  # noqa: D401
        self.total_assignments += 1
        self.generic_visit(node)


def analyze_code_complexity(code: str) -> StaticAnalysisResult:
    """Estimate complexity classes from code structure with explainable heuristics."""
    tree = ast.parse(code)
    visitor = ComplexityVisitor()
    visitor.visit(tree)

    if visitor.max_loop_depth >= 3:
        time_big_o = "O(n^3) or worse"
    elif visitor.max_loop_depth == 2:
        time_big_o = "O(n^2)"
    elif visitor.max_loop_depth == 1:
        time_big_o = "O(n)"
    else:
        time_big_o = "O(1) to O(log n)"

    if visitor.recursive_calls > 0 and visitor.max_loop_depth > 0:
        time_big_o = "O(n^2) to O(2^n) depending on recursion branching"
    elif visitor.recursive_calls > 0:
        time_big_o = "O(n) to O(2^n) depending on recursion branching"

    if visitor.dict_set_usage > 0 or visitor.list_comp_count > 0 or visitor.total_assignments > 8:
        space_big_o = "O(n)"
    else:
        space_big_o = "O(1)"

    explanation = (
        f"Detected max nested loop depth: **{visitor.max_loop_depth}**, "
        f"recursive call signals: **{visitor.recursive_calls}**, "
        f"list comprehensions: **{visitor.list_comp_count}**, "
        f"dict/set literals: **{visitor.dict_set_usage}**. "
        "Time complexity is inferred primarily from nesting and recursion patterns; "
        "space complexity is inferred from auxiliary collections and assignment pressure."
    )

    return StaticAnalysisResult(
        time_complexity=time_big_o,
        space_complexity=space_big_o,
        explanation=explanation,
        loop_depth=visitor.max_loop_depth,
        has_recursion=visitor.recursive_calls > 0,
        uses_heavy_structures=visitor.dict_set_usage > 0,
    )
