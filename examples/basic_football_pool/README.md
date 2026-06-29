# Basic Football Pool Example

This example uses fake in-memory data. It does not publish CSV fixtures, real teams, countries, private data, or API outputs.

Run it from the repository root:

```bash
python examples/basic_football_pool/run_example.py
```

It demonstrates the full framework flow and the public function used at each step:

| Step | What it demonstrates | Function |
| --- | --- | --- |
| 1 | Create anonymous football prediction options | local example data |
| 2 | Blend bookmaker and prediction-market style rows | `build_source_probability_table(...)` |
| 3 | Apply reviewed expert context | `apply_expert_signals(...)` |
| 4 | Estimate opponent pick behavior | `estimate_field_distribution(...)` |
| 5 | Add EV/leverage diagnostics | `add_value_diagnostics(...)` |
| 6 | Compare strategy portfolios | `run_betting_tournament_strategy(...)` |
| 7 | Build a risk-capped portfolio | `build_risk_capped_portfolio(...)` |

The printed output includes:

- ranked strategies
- recommended portfolio
- risk-capped portfolio
- rank distribution sample
- high-leverage options
