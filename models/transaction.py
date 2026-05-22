class Transaction:
    def __init__ (self, transaction_id, amount, date, description):
        self.id = transaction_id
        self.amount = amount
        self.date = date
        self.description = description

    def apply(self, balance):
        return balance
    
    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "date": self.date,
            "description": self.description
        }
