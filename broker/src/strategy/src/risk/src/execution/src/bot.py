from strategy.fvg_detector import FVGDetector
from strategy.order_block_detector import OrderBlockDetector
from strategy.liquidity_detector import LiquidityDetector
from risk.risk_manager import RiskManager
from execution.trade_executor import TradeExecutor


class CME_SMCBot:
    def __init__(self, broker):
        self.broker = broker
        self.fvg = FVGDetector()
        self.ob = OrderBlockDetector()
        self.liquidity = LiquidityDetector()
        self.executor = TradeExecutor(broker)

    def run(self, candles, balance):
        print("Scanning market...")

        fvgs = self.fvg.detect(candles)
        obs = self.ob.detect(candles)
        liquidity = self.liquidity.detect(candles)

        print(f"FVGs: {len(fvgs)}")
        print(f"Order Blocks: {len(obs)}")
        print(f"Liquidity Zones: {len(liquidity)}")

        # Trade logic will be added here.
