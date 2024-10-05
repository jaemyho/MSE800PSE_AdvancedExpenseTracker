from flask import render_template, request, redirect, url_for
from models.expenses_model import ExpensesModel
import datetime
class ExpenseController:
    def __init__(self, app):
        self.expenses_model = ExpensesModel(app)

    #Home page
    def index(self):
        return render_template('index.html')

    def add_expense(self):
        if request.method == 'POST':
            vendor = request.form['vendor']
            category = request.form['category']
            description = request.form['description']
            currency = request.form['currency']
            amount = request.form['amount']
            date = request.form['expense_date']
            self.expenses_model.add_expense(vendor, category, description, currency, amount, date)
            return redirect(url_for('add_expense'))  # Redirect to the add user page after successful submission
        return render_template('add_expense.html')

    def view_expense(self):
        expenses = self.expenses_model.get_all_expense()
        print(expenses)
        #expenses = ({'id': 1, 'user_id': 1, 'company_id': 1, 'category_id': 1, 'vendor': 'KFC', 'description': 'Breakfaswt', 'currency_id': 1, 'amount': 30.0, 'bank_statement': 0, 'date': datetime.date(2024, 10, 4), 'insert_date': datetime.datetime(2024, 10, 4, 0, 0)}, {'id': 2, 'user_id': 1, 'company_id': 1, 'category_id': 1, 'vendor': 'KFC', 'description': 'Breakfast', 'currency_id': 1, 'amount': 30.0, 'bank_statement': 0, 'date': datetime.date(2024, 10, 4), 'insert_date': datetime.datetime(2024, 10, 4, 0, 0)})
        return render_template('index.html')
        #return render_template('report.html', expenses=expenses)

    #