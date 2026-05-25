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

if __name__ == "__main__":
    unittest.main()
