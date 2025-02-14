# config.py
import os

# API keys and configuration
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', 'AKNZ2LJFKEG5WHYOC3YZ')
ALPACA_API_SECRET = os.getenv('ALPACA_API_SECRET', 'bc4fpy2fXek1gFgzxEMv98e6Zj5Zj7u12Gtot3zA')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')
# ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://api.alpaca.markets')

# Trading strategy parameters
SMA_SHORT_WINDOW = 50
SMA_LONG_WINDOW = 200

# Risk management parameters
STOP_LOSS_PERCENTAGE = 0.05
