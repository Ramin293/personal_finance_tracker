import json
import os

from models.income import Income
from models.expense import Expense

class FileHandler:
    def __init__(self,filename):
        self.filename = filename
        
    def save(self, transactions):
        folder = os.path.dirname(self.filename)

        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        data = []

        for transaction in transactions:
            data.append(transaction.to_dict())

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        
    def load(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError:
            return []

        transactions = []

        for item in data:
            transaction_type = item.get("type")

            if transaction_type == "income":
                transaction = Income(
                    item.get("id"),
                    item.get("amount"),
                    item.get("date"),
                    item.get("description")
                )
                transactions.append(transaction)

            elif transaction_type == "expense":
                transaction = Expense(
                    item.get("id"),
                    item.get("amount"),
                    item.get("date"),
                    item.get("description"),
                    item.get("category")
                )
                transactions.append(transaction)

        return transactions