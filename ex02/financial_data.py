"""Exercise 2: Apple stock, monthly aggregation and daily returns."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "AAPL.csv"

# 1. load the data: the dates are parsed as datetime and used as the index
df = pd.read_csv(DATA, parse_dates=["Date"], index_col="Date").sort_index()

missing_values = df.isna().sum()
df = df.dropna()

# 2. candlestick chart
candlestick = go.Figure(go.Candlestick(x=df.index,
                                       open=df["Open"],
                                       high=df["High"],
                                       low=df["Low"],
                                       close=df["Close"]))
candlestick.update_layout(title="Apple stock", xaxis_title="Date",
                          yaxis_title="Price ($)")

# 3. aggregate on the last business day of each month. The aggregation
# depends on the meaning of the variable: the prices are averaged, the High
# is the highest of the month, the Low the lowest, and the volumes are summed
transformed_df = df.resample("BME").agg({
    "Open": "mean",
    "Close": "mean",
    "Volume": "sum",
    "High": "max",
    "Low": "min",
    "Adj Close": "mean",
})
months = len(transformed_df)

# 4. daily returns on the Open price, without any loop
daily_returns = df["Open"].pct_change()
# the same computation, written with the formula of the subject
daily_returns_vectorized = (df["Open"] - df["Open"].shift(1)) / df["Open"].shift(1)

if __name__ == "__main__":
    print("1. missing values:", missing_values.to_dict())
    print(df.info(), end="\n\n")
    print(df.describe().to_markdown(), end="\n\n")

    candlestick.write_html(HERE / "candlestick.html", include_plotlyjs="cdn")
    try:
        candlestick.write_image(HERE / "candlestick.png")
    except Exception as error:  # the png export needs kaleido and Chrome
        print(f"candlestick.png not exported: {error}")
    candlestick.show()

    print("3. months in the period:", months)
    print(transformed_df.head()[["Open", "Close", "Volume", "High", "Low"]].to_markdown(),
          end="\n\n")
    print("4. daily returns:", daily_returns, sep="\n")
    # the two methods differ by at most 1e-16, which is the floating point noise
    print("both methods are equal:",
          np.allclose(daily_returns, daily_returns_vectorized, equal_nan=True))
