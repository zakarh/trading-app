# TRADING APP

## Running the app

Usage

Install Dependencies:

    pip install numpy pandas matplotlib pandas-datareader alpaca-trade-api

Configure API Keys:
Either update the keys in config.py or set the corresponding environment variables.

Run Backtesting:

Trend Following:

    python main.py --mode backtest --symbol AAPL --strategy trend

Mean Reversion:

    python main.py --mode backtest --symbol AAPL --strategy meanrev

Momentum:

    python main.py --mode backtest --symbol AAPL --strategy momentum

Run Live Trading (Paper Trading):

For example, to run a live Momentum strategy:

    python main.py --mode live --symbol AAPL --strategy momentum