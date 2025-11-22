class Finance():
    def __init__(self):
        self.currency = 0


    def addCurr(addAmount):
        self.currency+=addAmount

    def trySpendCurr(loseAmount):
        if (self.currency >= loseAmount):
            self.currency -= loseAmount
            return True
        else:
            return False

    