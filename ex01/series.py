"""Exercise 1: a daily Series and its 7 days moving average."""
import pandas as pd

dates = pd.date_range(start="2010-01-01", end="2020-12-31", freq="D")

# 1. the value is the number of days since the 1st January 2010
integer_series = pd.Series(range(len(dates)), index=dates, name="integer_series")

# 2. 7 days moving average, without any loop
moving_average = integer_series.rolling(window=7).mean()

if __name__ == "__main__":
    print("1.", integer_series, sep="\n", end="\n\n")
    print("2.", moving_average, sep="\n")
