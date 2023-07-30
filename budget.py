class Category:

    def __init__(self, budget_category):
        self.ledger = []
        self.budget_category = budget_category
    
    def get_balance(self):
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]
        return round(balance,2)

    def deposit(self, amount, description = ""):
        self.ledger.append({"amount": amount, "description": description})
    
    def check_funds(self,amount):
        return self.get_balance() >= amount

    def withdraw(self, amount, description = ""):
        if self.check_funds(amount) == True:
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False
    
    def transfer(self, amount, category):
        if self.check_funds(amount) == True:
            self.withdraw(amount, f"Transfer to {category.budget_category}")
            category.deposit(amount, f"Transfer from {self.budget_category}")
            return True
        else:
            return False


def create_spend_chart(categories):
