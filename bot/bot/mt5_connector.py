import MetaTrader5 as mt5
from datetime import datetime

from bot.config import (
    MT5_LOGIN,
    MT5_PASSWORD,
    MT5_SERVER,
    SYMBOL
)


class MT5Connector:

    def __init__(self):
        self.connected = False

    def connect(self):
        if not mt5.initialize():
            print("Failed to initialize MT5")
            return False

        authorized = mt5.login(
            login=MT5_LOGIN,
            password=MT5_PASSWORD,
            server=MT5_SERVER
        )

        if not authorized:
            print("Login failed")
            mt5.shutdown()
            return False

        self.connected = True
        print("Connected to MetaTrader 5")
        return True

    def disconnect(self):
        mt5.shutdown()
        self.connected = False

    def get_rates(self, timeframe, bars=500):
        rates = mt5.copy_rates_from_pos(
            SYMBOL,
            timeframe,
            0,
            bars
        )

        return rates

    def account_info(self):
        return mt5.account_info()

    def symbol_info(self):
        return mt5.symbol_info(SYMBOL)


if __name__ == "__main__":

    connector = MT5Connector()

    if connector.connect():

        print(connector.account_info())
        print(connector.symbol_info())

        connector.disconnect()
