from utils.validator import Validator
from datetime import datetime
from colorama import Fore, Back, Style


def clear_screen():
    print("\n" * 2)

def print_header(manager=None):
    print("=" * 50)
    print("            PERSONAL FINANCE TRACKER")
    print("=" * 50)

    if manager is not None:
        balance = manager.calculate_balance()

        if balance > 0:
            color = Fore.GREEN
        elif balance < 0:
            color = Fore.RED
        else:
            color = Fore.YELLOW

        print(f"Current balance: {color}{balance} tg{Style.RESET_ALL}")
        print("=" * 50)

def print_menu():
    print("\n             Chose an option:")
    print("            1. Add income.")
    print("            2. Add expense.")
    print("            3. Show transaction.")
    print("            4. Show category breakdown.")
    print("            5. Show monthly summary.")
    print("            6. Detect overspending.")
    print("            7. Detect transaction.")
    print("            8. Clear all data.")
    print("            0. Exit.")
    print("-" * 50)

def pause():
    input("\n Press enter to continue...")

def get_amount():
    while True:
        try:
            amount = input("Enter amount: ").replace(",", ".")
            amount = float(amount)

            if Validator.validate_amount(amount):
                return amount
            else:
                print("Amount must be greater than 0.")
        
        except ValueError:
            print("Invalid amount. Please enter a number.")

def get_date():
    while True:
        date = input("Enter date YYYY-MM-DD or press Enter for today: ")
        if date.strip()=="":
            return datetime.today().strftime("%Y-%m-%d")
        
        if Validator.validate_date(date):
            return date

        print("Invalid date format. Example: 2026-05-12")

def generate_transactiond_id(manager):
    if len(manager.transactions) == 0:
        return 1
    
    max_id = 0

    for transaction in manager.transactions:
        if transaction.id > max_id:
            max_id = transaction.id

    return max_id + 1