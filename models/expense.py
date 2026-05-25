from models.transaction import Transaction

class Expense(Transaction):
    def __init__(self, transaction_id, amount, date, description, category):
        super().__init__(transaction_id, amount, date, description)
        self.category = category
    
    def apply(self, balance):
        return balance - self.amount
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "expense"
        data["category"] = self.category
        return data
    