# backtest.py
import pandas as pd
import matplotlib.pyplot as plt
from data_fetcher import fetch_historical_data
import datetime
from strategy import compute_sma_signals, compute_mean_reversion_signals, compute_momentum_signals

def backtest_strategy(strategy_func, symbol, start_date, end_date, strategy_name='Strategy', **kwargs):
    """
    Backtest a given strategy function for a symbol over a specified period.
    """
    df = fetch_historical_data(symbol, start_date, end_date)
    if df is None:
        print("Failed to fetch data.")
        return

    df = strategy_func(df, **kwargs)

    # Calculate returns
    df['Market_Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Market_Returns'] * df['Position']

    # Compute cumulative returns
    df['Cumulative_Market'] = (1 + df['Market_Returns']).cumprod()
    df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod()

    # Plot performance
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Cumulative_Market'], label='Market Returns')
    plt.plot(df.index, df['Cumulative_Strategy'], label=f'{strategy_name} Returns')
    plt.legend()
    plt.title(f'Backtest Results for {symbol} using {strategy_name}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.show()

if __name__ == '__main__':
    symbol = 'AAPL'
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2021, 1, 1)

    print("Backtesting Trend Following Strategy")
    backtest_strategy(compute_sma_signals, symbol, start, end, strategy_name='Trend Following')

    print("Backtesting Mean Reversion Strategy")
    backtest_strategy(compute_mean_reversion_signals, symbol, start, end, strategy_name='Mean Reversion')

    print("Backtesting Momentum Strategy")
    backtest_strategy(compute_momentum_signals, symbol, start, end, strategy_name='Momentum')
