class TradeExecutor:
    def __init__(self, broker):
        self.broker = broker

    def buy(self, symbol, lot, sl, tp):
        return self.broker.place_order(
            symbol=symbol,
            order_type="BUY",
            volume=lot,
            stop_loss=sl,
            take_profit=tp
        )

    def sell(self, symbol, lot, sl, tp):
        return self.broker.place_order(
            symbol=symbol,
            order_type="SELL",
            volume=lot,
            stop_loss=sl,
            take_profit=tp
        )
