import MetaTrader5 as mt5

class MT5Connector:
    def __init__(self):
        self.connected = False

    def connect(self, login, password, server):
        if not mt5.initialize(login=login, password=password, server=server):
            print("MT5 initialization failed:", mt5.last_error())
            return False

        self.connected = True
        print("Connected to MetaTrader 5")
        return True

    def shutdown(self):
        mt5.shutdown()
        self.connected = False
