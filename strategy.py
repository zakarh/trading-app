# strategy.py
import pandas as pd
import numpy as np
from config import SMA_SHORT_WINDOW, SMA_LONG_WINDOW

def compute_sma_signals(df):
    """
    Trend Following strategy using moving average crossover.
    """
    df = df.copy()
    df['SMA_Short'] = df['Close'].rolling(window=SMA_SHORT_WINDOW).mean()
    df['SMA_Long'] = df['Close'].rolling(window=SMA_LONG_WINDOW).mean()
    df['Signal'] = 0
    df['Signal'].iloc[SMA_LONG_WINDOW:] = np.where(
        df['SMA_Short'].iloc[SMA_LONG_WINDOW:] > df['SMA_Long'].iloc[SMA_LONG_WINDOW:], 1, -1
    )
    df['Position'] = df['Signal'].shift(1)
    return df

def compute_mean_reversion_signals(df, window=20, num_std=2):
    """
    Mean Reversion strategy using Bollinger Bands.
    Buy when price is below the lower band (oversold).
    Sell when price is above the upper band (overbought).
    """
    df = df.copy()
    df['Rolling_Mean'] = df['Close'].rolling(window=window).mean()
    df['Rolling_Std'] = df['Close'].rolling(window=window).std()
    df['Upper_Band'] = df['Rolling_Mean'] + (num_std * df['Rolling_Std'])
    df['Lower_Band'] = df['Rolling_Mean'] - (num_std * df['Rolling_Std'])
    
    df['Signal'] = 0
    df.loc[df['Close'] < df['Lower_Band'], 'Signal'] = 1   # Buy signal
    df.loc[df['Close'] > df['Upper_Band'], 'Signal'] = -1  # Sell signal
    df['Position'] = df['Signal'].shift(1)
    return df

def compute_momentum_signals(df, momentum_period=10):
    """
    Momentum strategy based on price changes over a specified period.
    Buy if the price has increased (positive momentum); sell if decreased.
    """
    df = df.copy()
    df['Momentum'] = df['Close'].diff(momentum_period)
    df['Signal'] = np.where(df['Momentum'] > 0, 1, np.where(df['Momentum'] < 0, -1, 0))
    df['Position'] = df['Signal'].shift(1)  # Shift to avoid lookahead bias
    df = df.fillna(0) 
    return df

def get_latest_signal(strategy_func, current_data, historical_df, **kwargs):
    """
    Generic function to compute the latest signal using a strategy function.
    `strategy_func` should accept a DataFrame and return a DataFrame with a 'Signal' column.
    """
    new_row = pd.DataFrame([current_data])
    combined_df = pd.concat([historical_df, new_row], ignore_index=True)
    combined_df = strategy_func(combined_df, **kwargs)
    return combined_df.iloc[-1]['Signal']

if __name__ == '__main__':
    # Example usage for each strategy.
    import datetime
    from data_fetcher import fetch_historical_data
    symbol = 'AAPL'
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2021, 1, 1)
    df = fetch_historical_data(symbol, start, end)
    if df is not None:
        # Trend Following
        df_trend = compute_sma_signals(df)
        print("Trend Following Signals:")
        print(df_trend[['Close', 'SMA_Short', 'SMA_Long', 'Signal', 'Position']].tail())
        
        # Mean Reversion
        df_mean_rev = compute_mean_reversion_signals(df)
        print("\nMean Reversion Signals:")
        print(df_mean_rev[['Close', 'Rolling_Mean', 'Upper_Band', 'Lower_Band', 'Signal', 'Position']].tail())
        
        # Momentum
        df_momentum = compute_momentum_signals(df)
        print("\nMomentum Signals:")
        print(df_momentum[['Close', 'Momentum', 'Signal', 'Position']].tail())
