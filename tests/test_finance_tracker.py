import sys
import os
import unittest
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.income import Income
from models.expense import Expense
from services.finance_manager import FinanceManager
from services.file_handler import FileHandler
from services.budget_settings import BudgetSettings
from utils.console_ui import generate_transaction_id

class TestTransaction(unittest.TestCase):

    def test_income_apply_adds_money_to_balance(self):
        manager = FinanceManager()
        transaction_id = generate_transaction_id(manager)
        income = Income(transaction_id, 100000, "2026-05-13", "Salary")
        result = income.apply(50000)
        
        self.assertEqual(150000, result)

    def test_expense_apply_substracts_money_from_balance(self):
        manager = FinanceManager()
        transaction_id = generate_transaction_id(manager)
        expense = Expense(transaction_id, 5000, "2026-05-12", "KFC", "Food")
        result = expense.apply(50000)

        self.assertEqual(result, 45000)

    def test_data_is_saved_correctly(self):
        manager = FinanceManager()
        transaction_id = generate_transaction_id(manager)
        income = Income(transaction_id, 100000, "2026-05-12", "Salary")

        self.assertEqual(income.id, 1)
        self.assertEqual(income.description, "Salary")
        self.assertEqual(income.amount, 100000)
        self.assertEqual(income.date, "2026-05-12")

    def test_expense_data_is_saved_correctly(self):
        manager = FinanceManager()
        transaction_id = generate_transaction_id(manager)
        expense = Expense(transaction_id, 5000, "2026-05-12", "KFC", "Food")

        self.assertEqual(expense.id, 1)
        self.assertEqual(expense.description, "KFC")
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.amount, 5000)
        self.assertEqual(expense.date, "2026-05-12")

class TestFinanceManager(unittest.TestCase):
    def test_generate_transaction_id_for_empty_list(self):
        manager = FinanceManager()
        transaction_id = generate_transaction_id(manager)

        self.assertEqual(1, transaction_id)
    
    def test_generate_transaction_id_after_existing_transaction(self):
        manager = FinanceManager()
        first_id = generate_transaction_id(manager)
        income = Income(first_id, 100000, "2026-05-13", "Salary")
        manager.add_transaction(income)
        second_id = generate_transaction_id(manager)

        self.assertEqual(second_id, 2)

    def test_add_transaction(self):
        manager = FinanceManager()
        transaction_id = generate_transaction_id(manager)

        income = Income(transaction_id, 100000, "2026-05-13", "Salary")
        manager.add_transaction(income)

        self.assertEqual(len(manager.transactions), 1)
        self.assertEqual(manager.transactions[0].id, 1)
        self.assertEqual(manager.transactions[0].description, "Salary")

    def test_calculate_balance_with_income_and_expense(self):
        manager = FinanceManager()
        income_id = generate_transaction_id(manager)
        income = Income(income_id, 100000, "2026-05-13", "Salary")
        manager.add_transaction(income)

        expense_id = generate_transaction_id(manager)
        expense = Expense(expense_id, 5000, "2026-05-14", "KFC", "Food")
        manager.add_transaction(expense)

        balance = manager.calculate_balance()

        self.assertEqual(balance, 95000)

if __name__ == "__main__":
    unittest.main()
