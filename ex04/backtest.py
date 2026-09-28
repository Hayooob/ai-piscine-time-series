"""Exercise 4: backtest of a long only strategy on the Apple stock.

The signal at date d says whether the close price will increase at d+1. When
the signal is 1, 1$ of stock is bought just before the close and sold just
before the close of the next day; the profit is never reinvested.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "AAPL.csv"
OUTPUT = HERE / "daily_pnl.png"
CUMULATED_OUTPUT = HERE / "cumulated_pnl.png"

np.random.seed(2712)

# the index has to be sorted, otherwise the future return is wrong
df = pd.read_csv(DATA, parse_dates=["Date"], index_col="Date").sort_index()
missing_values = df.isna().sum()
df = df.dropna()


def compute_futur_return(price):
    """Return(t) = (Price(t+1) - Price(t)) / Price(t)."""
    return (price.shift(-1) - price) / price


# 1. daily future return on the adjusted close price
daily_futur_returns = compute_futur_return(df["Adj Close"])
daily_futur_returns.name = "Daily_futur_returns"

# 2. random signal: 1 means "buy 1$ of stock before the close"
long_only_signal = pd.Series(np.random.randint(0, 2, len(df.index)),
                             index=df.index, name="long_only_signal")

# 3. the PnL of a day is the future return when the signal is 1, else 0
pnl = (long_only_signal * daily_futur_returns).rename("PnL")

# 4. return of the strategy = (total earned - total invested) / total invested
invested = long_only_signal.sum()
strategy_return = pnl.sum() / invested

# 5. the same backtest with a signal that always buys
always_buy_signal = pd.Series(1, index=df.index, name="always_buy_signal")
pnl_always_buy = (always_buy_signal * daily_futur_returns).rename("PnL_always_buy")
invested_always_buy = always_buy_signal.sum()
return_always_buy = pnl_always_buy.sum() / invested_always_buy

if __name__ == "__main__":
    print("missing values:", missing_values.to_dict())
    print(df.info(), end="\n\n")
    print(df.describe().to_markdown(), end="\n\n")

    print("1. daily future returns:", daily_futur_returns, sep="\n", end="\n\n")
    print("2. signal:", long_only_signal.head(), sep="\n", end="\n\n")
    print("3. PnL:", pnl, sep="\n", end="\n\n")
    print(f"4. invested {invested}$, earned {invested + pnl.sum():.0f}$, "
          f"return of the strategy: {strategy_return}", end="\n\n")
    print(f"5. always buy: invested {invested_always_buy}$, "
          f"earned {invested_always_buy + pnl_always_buy.sum():.0f}$, "
          f"total PnL: {pnl_always_buy.sum():.2f}, return: {return_always_buy}")

    # the always buy PnL is drawn first, the random one on top of it: the two
    # are equal every day the random signal is 1
    ax = pd.concat([pnl_always_buy, pnl], axis=1).plot(
        title="Daily PnL: always buy vs random signal", linewidth=0.5, alpha=0.8)
    ax.set_ylabel("PnL ($)")
    ax.figure.tight_layout()
    ax.figure.savefig(OUTPUT)

    # the daily PnL of 40 years is dense; the cumulated PnL shows how the two
    # strategies compare over time
    ax = pd.concat([pnl_always_buy, pnl], axis=1).cumsum().plot(
        title="Cumulated PnL: always buy vs random signal")
    ax.set_ylabel("Cumulated PnL ($)")
    ax.figure.tight_layout()
    ax.figure.savefig(CUMULATED_OUTPUT)
    plt.show()
