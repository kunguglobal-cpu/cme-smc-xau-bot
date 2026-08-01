class TradeEngine:
    def __init__(self):
        pass

    def generate_signal(
        self,
        session_ok,
        cme_bias,
        market_bias,
        liquidity_swept,
        fvg_found,
        order_block_found
    ):
        if not session_ok:
            return "NO_TRADE"

        if (
            cme_bias == "BUY"
            and market_bias == "BUY"
            and liquidity_swept
            and (fvg_found or order_block_found)
        ):
            return "BUY"

        if (
            cme_bias == "SELL"
            and market_bias == "SELL"
            and liquidity_swept
            and (fvg_found or order_block_found)
        ):
            return "SELL"

        return "NO_TRADE"
