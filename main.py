from services.finance_manager import FinanceManager
from services.file_handler import FileHandler
from colorama import init
init(convert=True)
import os
os.system("")
from utils.console_ui import (
    clear_screen,
    print_header,
    print_menu,
    pause,
    add_income,
    add_expense,
    show_transactions_menu,
    show_category_breakdown,
    show_monthly_summary,
    detect_overspending,
    prepare_data_file,
    delete_transaction_by_id,
    clear_all_data
)

DATA_FILE = "data/transactions.json"

def main():
    prepare_data_file(DATA_FILE)
    file_handler = FileHandler(DATA_FILE)
    manager =  FinanceManager()
    manager.transactions = file_handler.load()

    while True:
        clear_screen()
        print_header(manager)
        print_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_income(manager, file_handler)
            pause()
        elif choice == "2":
            add_expense(manager, file_handler)
            pause()
        elif choice == "3":
            show_transactions_menu(manager)
            pause()
        elif choice == "4":
            show_category_breakdown(manager)
            pause()
        elif choice == "5":
            show_monthly_summary(manager)
            pause()
        elif choice == "6":
            detect_overspending(manager)
            pause()
        elif choice == "7":
            delete_transaction_by_id(manager, file_handler)
            pause()
        elif choice == "8":
            clear_all_data(manager, file_handler)
            pause()
        elif choice == "0":
            print("Goodbye!")
            pause()
        else:
            print("\nInvalid choice. Please, write a number according to the list")
            pause()

if __name__ == "__main__":
    main()

