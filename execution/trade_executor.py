class TradeExecutor:
    def __init__(self, broker):
        self.broker = broker

    def place_buy(self, symbol, lot, sl, tp):
        print(f"BUY {symbol} | Lot: {lot} | SL: {sl} | TP: {tp}")
        # TODO: Send order to MetaTrader 5

    def place_sell(self, symbol, lot, sl, tp):
        print(f"SELL {symbol} | Lot: {lot} | SL: {sl} | TP: {tp}")
        # TODO: Send order to MetaTrader 5
