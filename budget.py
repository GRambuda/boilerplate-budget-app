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

    def __str__(self):
        line_heading = f"{self.budget_category.center(30, '*')}\n"
        ledger_items = ['{:<23}{:>7}'.format(transaction["description"][:23],
            "{:.2f}".format(transaction["amount"]))
                        for transaction in self.ledger]
        total_balance = f"Total: {self.get_balance():.2f}"
        return line_heading + '\n'.join(ledger_items)+ '\n' + total_balance


def create_spend_chart(categories):
