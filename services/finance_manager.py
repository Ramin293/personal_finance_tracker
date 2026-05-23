from models.income import Income
from models.expense import Expense


class FinanceManager:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_all_transactions(self):
        return self.transactions

    def get_income_transactions(self):
        incomes = []

        for transaction in self.transactions:
            if isinstance(transaction, Income):
                incomes.append(transaction)

        return incomes

    def get_expense_transactions(self):
        expenses = []

        for transaction in self.transactions:
            if isinstance(transaction, Expense):
                expenses.append(transaction)

        return expenses

    def calculate_balance(self):
        balance = 0

        for transaction in self.transactions:
            balance = transaction.apply(balance)

        return balance

    def category_breakdown(self):
        result = {}

        for transaction in self.transactions:
            if isinstance(transaction, Expense):
                category = transaction.category
                result[category] = result.get(category, 0) + transaction.amount

        return result

    def delete_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                self.transactions.remove(transaction)
                return True

        return False

    def detect_overspending(self, limit):
        total_expenses = 0

        for transaction in self.transactions:
            if isinstance(transaction, Expense):
                total_expenses += transaction.amount

        if total_expenses > limit:
            return total_expenses - limit

        return 0