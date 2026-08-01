import MetaTrader5 as mt5


class MT5Broker:
    def __init__(self, login, password, server):
        self.login = login
        self.password = password
        self.server = server

    def connect(self):
        if not mt5.initialize():
            raise Exception("Failed to initialize MetaTrader 5")

        if not mt5.login(
            login=self.login,
            password=self.password,
            server=self.server
        ):
            raise Exception("Failed to log in to MT5")

        print("Connected to MetaTrader 5")

    def place_order(self, symbol, order_type, volume, stop_loss, take_profit):
        print(
            f"{order_type} {symbol} | Volume: {volume} | "
            f"SL: {stop_loss} | TP: {take_profit}"
        )

        # TODO: Replace this with a real mt5.order_send() request.
        return True

    def disconnect(self):
        mt5.shutdown()
