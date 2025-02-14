# live_trading.py
import time
import datetime
import pandas as pd
from data_fetcher import initialize_alpaca_api, fetch_live_data, fetch_historical_data
from strategy import (
    get_latest_signal,
    compute_momentum_signals,
)  # or any other strategy you prefer
from risk_management import check_stop_loss
from config import STOP_LOSS_PERCENTAGE


def place_order(api, symbol, qty, side, order_type="market", time_in_force="gtc"):
    """
    Place an order using the Alpaca API.

    Parameters:
        api: Initialized Alpaca API object.
        symbol (str): The ticker symbol (e.g., 'AAPL').
        qty (int): Quantity to trade.
        side (str): 'buy' or 'sell'.
        order_type (str): Order type (default is 'market').
        time_in_force (str): Order time in force (default is 'gtc').

    Returns:
        order: The submitted order object if successful; otherwise, None.
    """
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
        )
        print(f"Order submitted: {order}")
        return order
    except Exception as e:
        print("Order submission failed:", e)
        return None


def live_trading_loop(symbol, api, strategy_func, strategy_kwargs={}):
    """
    Main loop for live trading.

    Parameters:
        symbol (str): Trading symbol (e.g., 'AAPL').
        api: Initialized Alpaca API object.
        strategy_func: Function to compute trading signals (e.g., compute_momentum_signals).
        strategy_kwargs: Additional keyword arguments for the strategy function.
    """
    # Seed with historical data (e.g., one year back)
    start = datetime.datetime.now() - datetime.timedelta(days=365)
    end = datetime.datetime.now()
    historical_df = fetch_historical_data(symbol, start, end)

    in_position = False  # Track if currently holding a position
    last_order_price = None  # Price at which the last buy order was executed
    order_qty = 10  # Example quantity of shares

    while True:
        # Fetch the latest live data
        live_data = fetch_live_data(api, symbol)
        if live_data is None:
            print("Failed to fetch live data. Retrying in 60 seconds...")
            time.sleep(60)
            continue

        # Compute the latest signal using live data combined with historical data
        current_signal = get_latest_signal(
            strategy_func, live_data, historical_df, **strategy_kwargs
        )
        print(f"Current signal for {symbol}: {current_signal}")

        # Buy Order Logic: If a buy signal is generated and we're not already in a position.
        if current_signal == 1 and not in_position:
            print("Buy signal detected. Placing buy order.")
            order = place_order(api, symbol, order_qty, side="buy")
            if order is not None:
                last_order_price = live_data["close"]
                in_position = True

        # Sell Order Logic: If a sell signal is generated and we currently hold a position.
        elif current_signal == -1 and in_position:
            print("Sell signal detected. Placing sell order.")
            order = place_order(api, symbol, order_qty, side="sell")
            if order is not None:
                in_position = False
                last_order_price = None

        # Stop-Loss Logic: If in position, check if current price triggers the stop-loss condition.
        if in_position and last_order_price is not None:
            if check_stop_loss(
                last_order_price, live_data["close"], STOP_LOSS_PERCENTAGE
            ):
                print("Stop loss triggered. Placing sell order.")
                order = place_order(api, symbol, order_qty, side="sell")
                if order is not None:
                    in_position = False
                    last_order_price = None

        # Append the latest live data to historical data for continuous analysis
        new_data = pd.DataFrame([live_data])
        historical_df = pd.concat([historical_df, new_data], ignore_index=True)

        # Wait for a minute (or adjust the frequency as needed) before the next iteration.
        time.sleep(60)


if __name__ == "__main__":
    symbol = "OPEN"
    api = initialize_alpaca_api()
    if api:
        # For example, using the Momentum strategy with a period of 10
        live_trading_loop(
            symbol,
            api,
            compute_momentum_signals,
            strategy_kwargs={"momentum_period": 10},
        )
