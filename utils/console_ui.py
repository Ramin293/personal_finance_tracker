from models.income import Income
from models.expense import Expense
from utils.validator import Validator
from services.budget_settings import BudgetSettings
from datetime import datetime
from colorama import Fore, Back, Style
import os


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

def get_monthly_expenses(manager, month):
    total_expenses = 0

    for transaction in manager.transactions:
        if isnstance(transaction, Expense) and get_month_from_date(transaction.date) == month:
            total_expenses += transaction.amount
    return total_expenses

def get_month_from_date(date):
    date = str(date).strip()

    if len(date) >= 7 and date[4] == "-":
        return date[:7]
    
    return None

def print_overspending_message(total_expenses, limit, warning_percent):
    warning_amount = limit * warning_percent / 100
    print("\n" + "=" * 50)
    print("BUDGET CHECK")
    print("=" * 50)
    print(f"Monthly limit: {limit} tg")
    print(f"Warning level: {warning_percent}% ({warning_amount} tg)")
    print(f"Spent this month: {total_expenses} tg")

    if total_expenses > limit:
        overspent = total_expenses - limit
        print(Fore.RED + f"Limit exceeded by {overspent} tg." + Style.RESET_ALL)

    elif total_expenses >= warning_amount:
        remaining = limit - total_expenses
        print(Fore.YELLOW + f"Warning: you are close to your monthly limit." + Style.RESET_ALL)
        print(Fore.YELLOW + f"Money left before limit: {remaining} tg." + Style.RESET_ALL)
    
    else:
        remaining = limit - total_expenses
        print(Fore.GREEN + f"You are within the limit. Money left: {remaining} tg." + Style.RESET_ALL)
    
    print("=" * 50)

def check_overspending_after_expense(manager, expense):
    settings = BudgetSettings()

    if settings.monthly_limit <=0:
        return

    month = get_month_from_date(expense.date)

    if month is None:
        return

    total_expenses = get_monthly_expenses(manager, month)

    print_overspending_message(
        total_expenses,
        settings.monthly_limit,
        settings.warning_percent
    )

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

def show_category_breakdown(manager):
    clear_screen()
    print_header()
    print("CATEGORY BREAKDOWN")
    print("-" * 50)

    breakdown = manager.category_breakdown()

    if len(breakdown) == 0:
        print("No expenses yet.")
        return

    colors = [
        Back.RED,
        Back.YELLOW,
        Back.GREEN,
        Back.BLUE,
        Back.MAGENTA,
        Back.CYAN
    ]

    reset = Style.RESET_ALL
    bar_width = 50

    total = sum(breakdown.values())
    sorted_categories = sorted(breakdown.items(), key = lambda x : x[1], everse = True)

    bar = ""

    for index, category_data in enumerate(sorted_categories):
        category, amount = category_data
        blocks = round((amount/total) * bar_width)
        color = colors[index%len(colors)]
        bar += color + " " * blocks+reset 

    print("\n[" +bar+ "]")
    print()

    for index, category_data in enumate(sorted_categories):
        category, amount = category_data
        percent = (amount/total) * 100
        color = colors[index%len(colors)]

        print(f"{color} {reset}{category:<20} {percent:>5.1f} % {amount:>10,.0f} tg")

    print("-" * 50)
    print(f"{'TOTAL':<22} 100.0% {total:>10,.0f} tg")

def show_monthly_summary(manager):
    clear_screen()
    print_header()
    print("MONTHLY SUMMARY")
    print("-" * 50)

    month = input("Enter month in format YYYY-MM: ").strip()

    if len(month) != 7 or month[4] != "-":
        print("Invalid month format. Example: 2026-05")
        return

    total_income = 0
    total_expences = 0
    category_totals= {}

    for transaction in manager.ransactions:
        transaction_date = str(transaction.date).strip()

        if transaction_date.startswith(month):
            if instance(transaction, Income):
                total_income += transaction.amount

            elif isinstance(transaction, Expense):
                total_expenses += transaction.amount

                category = transaction.category
                category_totals[category] = category_totals.get(category, 0) + transaction.amount

            balance = total_income - total_expenses

            print("\nMonthly report:")
            print("-" * 50)
            print(f"Month: {month}")
            print(f"Total income: {total_income}tg")
            print(f"Total expenses: {total_expenses} tg")
            print(f"Balance for month: {balance} tg")
            print("\nExpenses by category:")

            if len(category_totals) == 0:
                print("No expenses in this month.")
            else:
                for category, total in category_totals.items():
                    print(f"{category}: {total} tg")

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

def prepare_data_file(data_file):
    os.makedirs("data", exist_ok = True)

    if not os.path.exists(data_file):
        with open(data_file, "w") as file:
            file.write("[]")

def clear_all_data(manager, file_handler):
    clear_screen()
    print_header(manager)

    print("CLEAR ALL DATA")
    print("-" * 50)

    confirm = input("Are you sure you want to delete all data? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Operation cancelled.")
        return
    
    manager.transaction.clear()
    file_handler.save(manager.transactions)

    budget_settings = BudgetSettings()
    budget_settings.update_settings(0, 80)

    print("All transactions and overspending settings were cleared successfully.")