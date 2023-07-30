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
    total_withdrawals = {}
    percentage_share = {}
    
    # get all the withdraws for each category
    for category in categories:
        for transactions in category.ledger:
            if transactions['amount'] < 0:
                if category.budget_category not in total_withdrawals.keys():
                    total_withdrawals.update(
                        {category.budget_category: transactions['amount']})
                else:
                    total_withdrawals[
                    category.budget_category] += transactions['amount']
    
    # calculate the total withdrawals for all provided categories
    total = 0
    for keys in total_withdrawals:
        total += total_withdrawals[keys]
    
    # calculate the percentage share of withdrawals for each category
    for keys in total_withdrawals:
        percentage_share.update({keys: int(((total_withdrawals[keys] / total)
                                            * 100) // 10) * 10})
    
    dict_chart = {}
    for category, percentage in percentage_share.items():
        for i in range(100, -1, -10):
            if i not in dict_chart.keys():
                dict_chart[i] = 'o  ' if i <= percentage else '   '
            elif i <= percentage:
                dict_chart[i] += 'o  '
            else:
                dict_chart[i] += '   '
    
    # prepare spending chart
    chart = []
    for keys in dict_chart.keys():
        chart.append('{:>3}| {}'.format(keys, dict_chart[keys]))

    category_list = [category.budget_category for category in categories]
    length = 0
    width = 0
    for item in category_list:
        if len(item) > length:
            length = len(item)
    
    for item in category_list:
        width += 1

    for i in range(len(category_list)):
        if len(category_list[i]) < length:
            category_list[i] += ' ' * (length - len(category_list[i]))
        else:
            continue

    category_labels = []
    for n in range(length):
        category_labels.append ((' ' * 5) + 
                                '  '.join(category_list[i][n] for i in range(
                                    width)) + '  ')            

    # Print out the spending chart
    return ("Percentage spent by category\n" + 
            "\n".join(chart) + 
            f"\n    -{'-' * len(category_list) * 3}\n" +
           "\n".join(category_labels))