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