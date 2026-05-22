import Transaction

class Income(Transaction):
    def apply(self, balance):
        return self.amount + balance
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "income"
        return data
    