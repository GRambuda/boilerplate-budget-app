class Category:

    def __init__(self, budget_category):
        self.ledger = []
        self.budget_category = budget_category
    
    def get_balance(self):
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]
        return round(balance,2)


def create_spend_chart(categories):
