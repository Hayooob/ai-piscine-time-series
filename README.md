# Time series

Solutions for the Time series day of the AI piscine: manipulating a time
indexed Series, financial data, multi asset returns and a backtest.

## Structure

```
.
├── data/AAPL.csv                  # Apple stock, 1980-12-12 to 2021-01-29
├── ex00/
│   ├── requirements.txt
│   └── Notebook_ex00.ipynb
├── ex01/series.py
├── ex02/financial_data.py         -> candlestick.html / candlestick.png
├── ex03/multi_asset_returns.py
└── ex04/backtest.py               -> daily_pnl.png, cumulated_pnl.png
```

## Virtual environment (ex00)

```bash
python -m venv env/ex00
source env/ex00/Scripts/activate      # Windows (Git Bash); Linux/macOS: source env/ex00/bin/activate
pip install -r ex00/requirements.txt
python --version
python -c "import jupyter, numpy, pandas"
```

Tested with Python 3.13, pandas 3.0.6, NumPy 2.5.3 and plotly 7.1.0.
`matplotlib`, `tabulate` and `kaleido` are also installed: the plot of ex04,
the markdown tables and the png export of the plotly figures.

## Data

`AAPL.csv` comes from the
[01-edu subject](https://github.com/01-edu/public/tree/master/subjects/ai/time-series/data).

## Running an exercise

```bash
python ex02/financial_data.py
```

## Notes

- **ex02** — the aggregation is done on the last business day of each month
  (`resample("BME")`), which gives **482 months**. Each variable is
  aggregated according to its meaning: the prices are averaged, `High` takes
  the maximum, `Low` the minimum and `Volume` the sum.
- **ex02** — the daily returns are computed twice, with `pct_change` and with
  the formula of the subject (`shift`). The two differ by at most 1e-16,
  which is floating point noise, so they are compared with `np.allclose`.
- **ex03** — `pivot_table` puts one ticker per column, then `pct_change`
  computes the returns of the five assets at once. Shape: (261, 5).
- **ex04** — the index is sorted before computing the future return; on an
  unsorted index the result would be wrong. The PnL is `signal * future
  return`, so no loop is needed.
- **ex04** — the "always buy" strategy earned 10129$ for 10118$ invested, a
  return of 0.11%. The random signal gives a return close to 0, as expected.
  Its exact value depends on the random draw.
- **ex04** — besides the daily PnL asked by the subject, the cumulated PnL is
  plotted: on 40 years of daily data the two daily series overlap too much to
  be read, while the cumulated view shows that buying every day ends around
  11$ against 5$ for the random signal.

## Pandas 3 note

`resample("BM")` no longer exists, the code uses the current alias
`resample("BME")` (business month end).
