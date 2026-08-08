# bot/config.py

# ============================
# Broker Settings
# ============================
MT5_LOGIN = 12345678          # Replace with your MT5 account number
MT5_PASSWORD = "YOUR_PASSWORD"
MT5_SERVER = "FBS-Demo"       # Change to your actual FBS server

# ============================
# Trading Settings
# ============================
SYMBOL = "XAUUSD"
TIMEFRAME = "M5"

# ============================
# Risk Management
# ============================
RISK_PERCENT = 1.0
MAX_OPEN_TRADES = 1

# ============================
# Session Filter (UTC)
# ============================

# ============================
# Strategy Settings
# ============================
USE_CME_EXPECTED_RANGE = True
USE_FAIR_VALUE_GAP = True
USE_ORDER_BLOCK = True
USE_LIQUIDITY_SWEEP = True
USE_MARKET_STRUCTURE = True

# ============================
# Trade Management
# ============================
MIN_RISK_REWARD = 2.0
MOVE_TO_BREAK_EVEN = True
TRAILING_STOP = False

# ============================
# Logging
# ============================
LOG_LEVEL = "INFO"
