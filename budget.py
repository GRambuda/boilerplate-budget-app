class Category:
    """
    A class representing a budget category.

    Attributes:
        budget_category (str): The name of the budget category.
        ledger (list): A list of transactions in the form of 
                       {"amount": amount, "description": description}.
    """

    def __init__(self, budget_category):
        """
        Initialize a new budget category.

        Args:
            budget_category (str): The name of the budget category.
        """
        self.ledger = []
        self.budget_category = budget_category
    
    def get_balance(self):
        """
        Get the current balance of the budget category.

        Returns:
            float: The current balance.
        """
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]
        return round(balance,2)

    def deposit(self, amount, description = ""):
        """
        Record a deposit transaction in the ledger.

        Args:
            amount (float): The amount of the deposit.
            description (str, optional): The description of the deposit 
                                         (default is an empty string).

        Returns:
            None
        """
        self.ledger.append({"amount": amount, "description": description})
    
    def check_funds(self,amount):
        """
        Check if there are enough funds in the budget category for the 
        specified amount.

        Args:
            amount (float): The amount to check.

        Returns:
            bool: True if there are enough funds, False otherwise.
        """
        return self.get_balance() >= amount

    def withdraw(self, amount, description = ""):
        """
        Record a withdrawal transaction in the ledger.

        Args:
            amount (float): The amount of the withdrawal.
            description (str, optional): The description of the withdrawal 
                                         (default is an empty string).

        Returns:
            bool: True if the withdrawal took place, False otherwise.
        """
        if self.check_funds(amount) == True:
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    
    def transfer(self, amount, category):
        """
        Transfer an amount from this budget category to another.

        Args:
            amount (float): The amount to transfer.
            other_category (Category): The destination budget category.

        Returns:
            bool: True if the transfer took place, False otherwise.
        """
        if self.check_funds(amount) == True:
            self.withdraw(amount, f"Transfer to {category.budget_category}")
            category.deposit(amount, f"Transfer from {self.budget_category}")
            return True
        return False

    def __str__(self):
        """
        Return a string representation of the budget category.

        Returns:
            str: The formatted string representation of all transactions in
                 the budget category.
        """
        line_heading = f"{self.budget_category.center(30, '*')}\n"
        ledger_items = ['{:<23}{:>7}'.format(transaction["description"][:23],
            "{:.2f}".format(transaction["amount"]))
                        for transaction in self.ledger]
        total_balance = f"Total: {self.get_balance():.2f}"
        return line_heading + '\n'.join(ledger_items)+ '\n' + total_balance


def create_spend_chart(categories):
    """
    Builds a bar chart represention of the percentage spent in each given
    category.

    Args:
        categories (list): A list of budget categories.

    Returns:
        str: The formatted string representation of each withdrawal as a
             percentage of total withdrawals in a bar chart. 
    """
    total_withdrawals = {}
    percentage_share = {}
    
    # get all the withdraws for each category
    for category in categories:
        for transactions in category.ledger:
            if transactions['amount'] < 0:
                if category.budget_category not in total_withdrawals.keys():
                    total_withdrawals.update(
                        {category.budget_category: transactions['amount']})
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