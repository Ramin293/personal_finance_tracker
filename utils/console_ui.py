from models.income import Income
from models.expense import Expense
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

def generate_transaction_id(manager):
    if len(manager.transactions) == 0:
        return 1
    
    max_id = 0

    for transaction in manager.transactions:
        if transaction.id > max_id:
            max_id = transaction.id

    return max_id + 1

def add_income(manager, file_handler):
    clear_screen()
    print_header()
    print("ADD INCOME")
    print("-" * 50)

    description = input("Enter description: ")
    amount = get_amount()
    date = get_date().strip()
    transaction_id = generate_transaction_id(manager)

    income = Income(transaction_id, amount, date, description)
    manager.add_transactions(income)

    file_handler.save(manager.transactions)

    print("\nIncome added successfully.")
    print(f"ID: {income.id}")
    print(f"Description: {description}")
    print(f"Amount: {amount} tg")
    print(f"Date: {date}")
    
def add_expense(manager, file_handler):
    clear_screen()
    print_header()
    print("ADD EXPENSE")
    print("-" * 50)

    description = input("Enter description: ")

    while True:
        category = input("Enter category: ")

        if Validator.validate_category(category):
            break

        print("Category cannot be empty.")

    amount = get_amount()
    date = get_date()

    transaction_id = generate_transaction_id(manager)

    expense = Expense(transaction_id, amount, date, description, category)
    manager.add_transaction(expense)

    file_handler.save(manager.transaction)

    print("\nExpense added successfully.")
    print(f"ID: {expense.id}")
    print(f"Description: {description}")
    print(f"Category: {category}")
    print(f"Amount: {amount} tg")
    print(f"Date: {date}")

    check_overspending_after_expense(manager, expense)

def show_transactions_menu(manager):
    clear_screen()
    print_header()
    print("SHOW TRANSACTIONS")
    print("-" * 50)

    print("Choose transaction type: ")
    print("1. Income")
    print("2. Expense")
    print("3. All transactions")
    print("0. Back")
    print("-" * 50)

    choice = input("Enter your choice: ")

    if choice == "1":
        show_filtered_transactions(manager, "income")

    elif choice == "2":
        show_filtered_transactions(manager, "expense")

    elif choice == "3":
        show_filtered_transactions(manager, "all")

    elif choice == "0":
        return
    
    else:
        print("\nInvalid choice")

def show_filtered_transactions(manager, transaction_type):
    clear_screen()
    print_header()

    if transaction_type == "income":
        print("INCOME TRANSACTIONS")
    elif transaction_type == "expense":
        print("EXPENSE TRANSACTIONS")
    elif transaction_type == "all":
        print("ALL TRANSACTIONS")

    print("-" * 50)

    if len(manager.transactions) == 0:
        print("No transactions yet.")
        return
    
    month = input("Enter month in format YYYY-MM or press Enter to show all: ").strip()

    if month != "":
        if len(month) != 7 or month[4] != "-":
            print("Invalid month format. Example: 2025-05")
            return
        
    found = False

    for transaction in manager.transactions:
        transaction_date = str(transaction.date).strip()

        if month != "" and not transaction_date.startswith(month):
            continue

        if transaction_type == "income" and not isinstance(transaction,Income):
            continue

        if transaction_type == "expense" and not isinstance(transaction, Expense):
            continue

        found = True  
        if isinstance(transaction, Income):
            print(f"ID {transaction.id} | INCOME")
            print(f"Date: {transaction.date}")
            print(f"Description: {transaction.description}")
            print(f"Amount: +{transaction.amount} tg")

        elif isinstance(transaction, Expense):
            print(f"ID {transaction.id} | EXPENSE")
            print(f"Date: {transaction.date}")
            print(f"Description: {transaction.description}")
            print(f"Category: {transaction.category}")
            print(f"Amount: -{transaction.amount} tg")

        print("-" * 50)

    if not found:
        if transaction_type == "income":
            print("No income transactions found.")
        elif transaction_type == "expense":
            print("No expense transactions found.")
        else:
            print("No transactions found.")

def delete_transaction_by_id(manager, file_handler):
    clear_screen()
    print_header()
    print("DELETE TRANSACTION BY ID")
    print("-" * 50)

    if len (manager.transactions) == 0:
        print("No transactions yet.")
        return
    
    try:
        transaction_id = int(input("Enter transaction ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
    
    transaction_to_delete = None

    for transaction in manager.transactions:
        if transaction.id == transaction_id:
            transaction_to_delete = transaction
            break

    if transaction_to_delete is None:
        print(f"No transaction found with ID {transaction_id}.")
        return
    
    print("\nTransaction found: ")
    print("-" * 50)

    if isinstance(transaction_to_delete, Income):
        print(f"ID {transaction_to_delete.id} | INCOME")
        print(f"Description: {transaction_to_delete.description}")
        print(f"Amount: +{transaction_to_delete.amount} tg")
        print(f"Date: {transaction_to_delete.date}")

    elif isinstance(transaction_to_delete, Expense):
        print(f"ID {transaction_to_delete.id} | EXPENSE")
        print(f"Description: {transaction_to_delete.description}")
        print(f"Category: {transaction_to_delete.category}")
        print(f"Amount: -{transaction_to_delete.amount} tg")
        print(f"Date: {transaction_to_delete.date}")

    confirm = input("\nAre you sure you want to delete this transaction? yes/no: ")

    if confirm.lower() == "yes":
        manager.transactions.remove(transaction_to_delete)
        file_handler.save(manager.transactons)
        print("\nTransaction deleted successfully.")
        print("Data saved automatically.")

    else:
        print("\nAction cancelled")
