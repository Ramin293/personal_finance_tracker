from models.income import Income
from models.expense import Expense


class StatisticsService:
    @staticmethod
    def total_income(transactions):
        total = 0

        for transaction in transactions:
            if isinstance(transaction, Income):
                total += transaction.amount

        return total

    @staticmethod
    def total_expenses(transactions):
        total = 0

        for transaction in transactions:
            if isinstance(transaction, Expense):
                total += transaction.amount

        return total

    @staticmethod
    def monthly_summary(transactions, month):
        total_income = 0
        total_expenses = 0
        category_totals = {}

        for transaction in transactions:
            transaction_date = str(transaction.date).strip()

            if transaction_date.startswith(month):
                if isinstance(transaction, Income):
                    total_income += transaction.amount

                elif isinstance(transaction, Expense):
                    total_expenses += transaction.amount

                    category = transaction.category
                    category_totals[category] = category_totals.get(category, 0) + transaction.amount

        return {
            "month": month,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": total_income - total_expenses,
            "category_totals": category_totals
        }