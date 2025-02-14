# main.py
import argparse
import datetime
from backtest import backtest_strategy
from live_trading import live_trading_loop
from data_fetcher import initialize_alpaca_api
from strategy import compute_sma_signals, compute_mean_reversion_signals, compute_momentum_signals

def main():
    parser = argparse.ArgumentParser(description="Algorithmic Trading Tool")
    parser.add_argument('--mode', choices=['backtest', 'live'], required=True,
                        help="Choose mode: 'backtest' or 'live'")
    parser.add_argument('--symbol', type=str, default='AAPL', help="Trading symbol (default: AAPL)")
    parser.add_argument('--strategy', choices=['trend', 'meanrev', 'momentum'], default='trend',
                        help="Strategy to use: trend (SMA), meanrev (Mean Reversion), momentum (Momentum)")
    args = parser.parse_args()

    if args.mode == 'backtest':
        start = datetime.datetime(2020, 1, 1)
        end = datetime.datetime(2022, 1, 1)
        if args.strategy == 'trend':
            backtest_strategy(compute_sma_signals, args.symbol, start, end, strategy_name='Trend Following')
        elif args.strategy == 'meanrev':
            backtest_strategy(compute_mean_reversion_signals, args.symbol, start, end, strategy_name='Mean Reversion')
        elif args.strategy == 'momentum':
            backtest_strategy(compute_momentum_signals, args.symbol, start, end, strategy_name='Momentum')
    elif args.mode == 'live':
        api = initialize_alpaca_api()
        if api is None:
            print("Error: Could not initialize Alpaca API.")
            return
        # Select strategy for live trading
        if args.strategy == 'trend':
            strat_func = compute_sma_signals
            strat_kwargs = {}
        elif args.strategy == 'meanrev':
            strat_func = compute_mean_reversion_signals
            strat_kwargs = {'window': 20, 'num_std': 2}
        elif args.strategy == 'momentum':
            strat_func = compute_momentum_signals
            strat_kwargs = {'momentum_period': 10}
        live_trading_loop(args.symbol, api, strat_func, strategy_kwargs=strat_kwargs)

if __name__ == '__main__':
    main()
