# bot/cme_reader.py

class CMEReader:
    def __init__(self):
        self.expected_high = None
        self.expected_low = None

    def update_range(self, high, low):
        self.expected_high = high
        self.expected_low = low

    def get_range(self):
        return {
            "high": self.expected_high,
            "low": self.expected_low
        }

if __name__ == "__main__":
    cme = CMEReader()
    cme.update_range(3350.00, 3315.00)
    print(cme.get_range())
