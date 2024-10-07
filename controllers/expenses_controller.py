from flask import render_template, request, redirect, url_for
from models.expenses_model import ExpensesModel
import datetime
class ExpenseController:
    def __init__(self, mysql):
        self.expenses_model = ExpensesModel(mysql)

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
        return render_template('report.html', expenses=expenses)

    def get_receipt_total(self):
        return render_template('upload_file.html')
        # receipt_total = self.expenses_model.scan_receipt()
        # return receipt_total
