# Personal Finance Tracker

1. Ramin - models, validator, tests
2. Arnur - services
3. Arai - console_ui
4. Sulukhan - console_ui

## 1.Project overview

Personal finance tracker is a console python application for managing income, expense, monthly summary, category statistics and budget limits.

Our project application allows user a special opportunities like:

1. add income transactions
2. add expense transactions
3. automatically calculate the current balance
4. filter transactions by type and month
5. view expenses by category
6. generate montly summary
7. set a monthly limit with special warning message
8. delete transaction by ID
9. clear all data

## 2.Main goal of the finance tracker

The main goal of our project is to help users control their personal finances in consol form.

The program solves a practical problems such as going over monthly limits.

This project helps users answer the following questions:
- How much money did I spend for food?
- Which categories take the largest amount of money?
- Did I exceed my montly expense limit?

## 3.Technology Stack

The project contain following technologies:

1. **Python** used as main programming language
2. **Object-oriented programming** used as classes for transactions, incomes and expenses
3. **JSON** used for saving and loading data
4. **unittest** used for testing project
5. **colorama** used for colored output in console
6. **datetime** used for working with dates
7. **re** used for validating date format with regular expressions
8. **os** used for creating and checking project files

## 4.Project structure

1. main.py - main file, where program starts executing
2. README.md - file with description of the project

**data**
1. transactions.json - file with user information about transactions
2. budget_settings.json - file with user information about monthly limits

**models** 
1. income.py - class, which increases the current balance
2. expense.py - class, which decreases the current balance
3. transaction.py - class, which stores common transaction data

**servises**
1. finance_manager.py - servise class, which manages all transactions
2. file_handler.py - servise class, which saves and loads all data to transactions.json
3. budget_settings.py - servise class, which saves and loads data to budget_settings.json
4. statistics_servise.py - servise class, which calculates the statistics

**utils**
1. console_ui.py - main console interface file, which represents UI elements to console
2. validator.py - main validating file, which checks all user inputs

**tests**
1. test_finance_tracker.py - file with unit tests for the project

## 7.Main features

### 7.1. add income

The user enters following data:

- description
- amount
- date

The program automatically creates ID for transactions

Sample output:

```
ID: 1
Description: Salary
Amount: 250000
Date: 2026-05-01
```

### 7.2 add expense

The user enters following data:

- description
- category
- amount
- date

The program automatically creates ID for transactions

Sample output:

```
ID: 2
Description: KFC
Category: Food
Amount: 5470
Date: 2026-05-12
```

### 7.3 Show all transactions

The user choose one option:

```
1. Income
2. Expense
3. All transactions
0. Back
```

Transactions filtered by month

Sample input:

```
3
```

```
2026-05
```

Sample output:

```
ID: 1
Description: Salary
Amount: 250000
Date: 2026-05-01

ID: 2
Description: KFC
Category: Food
Amount: 5470
Date: 2026-05-12
```

### 7.4 Category breakdown

The function shows how much money was spent in each category

It also shows a colored bar in the colsole to make result easier

Sample output:

```
Food         45%    45000 tg
Transport    20%    20000 tg
Shopping     35%    35000 tg
```

### 7.5 Monthly summary

The user enters a month

``` 
2026-05
```

Sample output:

```
Month: 2026-05
Total income: 250000 tg
Total expenses: 75000 tg
Balance for month: 175000 tg

Expenses by category:
Food: 30000 tg
Transport: 15000 tg
Shopping: 30000 tg
```

### 7.6. Detecting overspending

This function allows user to set budget control settings

The user enters:

- monthly expense limit
- warning percent

Sample input

```
Monthtly limit: 200000 tg
Warning percent: 80%
```

Sample output:

```
Overspending settings saved successfully.
Monthly limit: 200000.0 tg
Warning percent: 80.0%

Current month check: 2026-05

==================================================
BUDGET CHECK
==================================================
Monthly limit: 200000.0 tg
Warning level: 80.0% (160000.0 tg)
Spent this month: 0 tg
You are within the limit. Money left: 200000.0 tg.
==================================================
```

### 7.7 Delete transaction

The user enters an ID of transaction

The program:

1. searches for the transaction;
2. shows the transaction details;
3. asks for confirmation;
4. deletes the transaction if the user types `yes`;
5. saves the updated data to JSON.

### 7.8 Clear all data

This function removes all transactions from project

## 8.Conclusion

Personal finance tracker is a practical Python console application that helps users manage incomes, expenses, balance and spending limits








