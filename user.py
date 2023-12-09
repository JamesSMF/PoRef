from math import inf

class User:
    def __init__(self, name, reputation = 0, money = 0):
        self.id = name
        self.reputation = reputation
        self.money = money

    def validate_succcess(self):
        self.reputation += 5
        self.money += 100

    def advocate_success(self):
        self.reputation += 2

    def punish(self):
        self.reputation = -inf
