import re

class Validator:
    @staticmethod
    def validate_amount(amount):
        return amount > 0
    
    @staticmethod
    def validate_date(date):
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        return re.match(pattern, date) is not None
    
    @staticmethod
    def validate_transaction_type(transaction_type):
        return transaction_type in ["income", "expense"]
    
    @staticmethod
    def validate_category(category):
        return len(category.strip()) > 0