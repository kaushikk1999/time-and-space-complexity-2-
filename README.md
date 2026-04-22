# Python Complexity Coach (Streamlit)

A portfolio-ready Streamlit app for interview practice that combines:
- AST-based time/space complexity heuristics
- Runtime and memory benchmarking (`time.perf_counter`, `tracemalloc`)
- Optimization scoring + actionable suggestions
- Deterministic code rewrite proposal
- Optional Gemini-enhanced feedback

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud

1. Push this repo to GitHub.
2. Create a new Streamlit Cloud app and point it to `app.py`.
3. Add optional secret `GEMINI_API_KEY` if you want Gemini insights.

## Notes

- Complexity estimation is heuristic and educational, not a formal proof.
- Execution uses restricted builtins but should still be treated as untrusted-code simulation, not full isolation.
