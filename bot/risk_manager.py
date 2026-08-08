class RiskManager:
    def __init__(self, risk_percent=1.0):
        self.risk_percent = risk_percent

    def calculate_lot_size(self, account_balance, stop_loss_points, value_per_point=1.0):
        """
        Calculate position size based on account risk.
        """

        if stop_loss_points <= 0:
            return 0.0

        risk_amount = account_balance * (self.risk_percent / 100)

        lot_size = risk_amount / (stop_loss_points * value_per_point)

        return round(max(lot_size, 0.01), 2)

    def calculate_stop_loss(self, sweep_level, buffer_points=50):
        """
        Place stop loss beyond the liquidity sweep.
        """
        return sweep_level - buffer_points

    def calculate_take_profit(self, target_level):
        """
        Take profit at the selected target level.
        """
        return target_level


if __name__ == "__main__":
    rm = RiskManager(risk_percent=1)

    balance = 10000
    stop_loss_points = 250

    lot = rm.calculate_lot_size(balance, stop_loss_points)

    print("Lot Size:", lot)
    print("SL:", rm.calculate_stop_loss(3300))
    print("TP:", rm.calculate_take_profit(3365))
