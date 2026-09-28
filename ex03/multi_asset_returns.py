"""Exercise 3: daily returns of several assets at once (no for loop)."""
import numpy as np
import pandas as pd

np.random.seed(42)

business_dates = pd.bdate_range('2021-01-01', '2021-12-31')

# generate tickers
tickers = ['AAPL', 'FB', 'GE', 'AMZN', 'DAI']

# create indexs
index = pd.MultiIndex.from_product([business_dates, tickers], names=['Date', 'Ticker'])

# create DFs
market_data = pd.DataFrame(index=index,
                           data=np.random.randn(len(index), 1),
                           columns=['Price'])

# one column per ticker, then the returns of every column at once
returns = market_data.pivot_table(values="Price", index="Date",
                                  columns="Ticker").pct_change()

if __name__ == "__main__":
    print("shape:", returns.shape)
    print(returns.head())
