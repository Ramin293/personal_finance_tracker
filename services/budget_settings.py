import json
import os

class BudgetSettings:
    def __init__(self, file_path="data/budget_settings.json"):
        self.file_path = file_path
        self.monthly_limit = 0
        self.warning_percent = 80

        self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.file_path):
            self.save_settings()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.monthly_limit = float(data.get("monthly_limit", 0))
            self.warning_percent = float(data.get("warning_percent", 80))

        except json.JSONDecodeError:
            self.monthly_limit = 0
            self.warning_percent = 80
            self.save_settings()

    def save_settings(self):
        folder = os.path.dirname(self.file_path)

        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        data = {
            "monthly_limit": self.monthly_limit,
            "warning_percent": self.warning_percent
        }

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def update_settings(self, monthly_limit, warning_percent):
        self.monthly_limit = monthly_limit
        self.warning_percent = warning_percent
        self.save_settings()

    def reset_settings(self):
        self.monthly_limit = 0
        self.warning_percent = 80
        self.save_settings()