class RiskManager:
    def __init__(self, balance, risk_percent=1.0):
        self.balance = balance
        self.risk_percent = risk_percent

    def risk_amount(self):
        return self.balance * (self.risk_percent / 100)

    def calculate_lot_size(self, stop_loss_points, value_per_point):
        if stop_loss_points <= 0 or value_per_point <= 0:
            return 0.0

        risk = self.risk_amount()
        lot_size = risk / (stop_loss_points * value_per_point)
        return round(lot_size, 2)
