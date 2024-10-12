from flask import render_template, request, redirect, url_for
from models.expenses_model import ExpensesModel
from file_upload_handler import FileUploadHandler
from receipt_reader import ReceiptReader
from sql_statement import *
import pandas as pd
from bank_statement_reader import BankStatementReader
from controllers.currency_controller import CurrencyController
from controllers.category_controller import CategoryController

class ExpenseController:
    def __init__(self, mysql,app):
        self.app = app
        self.expenses_model = ExpensesModel(mysql,app)
        self.currency_controller = CurrencyController(mysql)
        self.category_controller = CategoryController(mysql)

    #Home page
    def index(self):
        return render_template('index.html')

    def add_expense(self):
        currencies = self.currency_controller.get_all_currencies()
        categories = self.category_controller.get_all_categories()
        if request.method == 'POST':
            vendor = request.form['vendor']
            category = request.form['category']
            description = request.form['description']
            currency = request.form['currency']
            amount = request.form['amount']
            date = request.form['expense_date']
            receipt = 0
            self.expenses_model.add_expense(vendor, category, description, currency, amount, date,receipt)
            return redirect(url_for('add_expense'))  # Redirect to the add user page after successful submission
        return render_template('expense.html', title='Add Expense', expense="", currencies=currencies, categories=categories)

    def edit_expense(self, expense_id):
        expense = self.expenses_model.get_expense_by_id(expense_id)
        currencies = self.currency_controller.get_all_currencies()
        categories = self.category_controller.get_all_categories()
        if request.method == 'POST':
            vendor = request.form['vendor']
            category = request.form['category']
            description = request.form['description']
            currency = request.form['currency']
            amount = request.form['amount']
            date = request.form['expense_date']
            self.expenses_model.update_expense(expense_id, vendor, category, description, currency, amount, date, expense)
            return redirect(url_for('report'))
        return render_template('expense.html', title='Edit Expense',expense=expense, currencies=currencies, categories=categories)

    def delete_expense(self, expense_id):
        expense = self.expenses_model.get_expense_by_id(expense_id)
        currencies = self.currency_controller.get_all_currencies()
        categories = self.category_controller.get_all_categories()
        if request.method == 'POST':
            self.expenses_model.delete_expense(expense_id,expense)
            return redirect(url_for('report'))
        return render_template('expense.html', title='Delete Expense', expense=expense, currencies=currencies, categories=categories)

    def view_expense(self):
        sql = GET_ALL_EXPENSES
        type, start_date, end_date, grouped_dict_category = "", "", "", {}
        if request.method == 'POST':
            type = request.form['search_type']
            start_date = request.form['search_start']
            end_date = request.form['search_end']

            sql = sql[:-1]  # removing character ";" at the end
            sql += " WHERE 1=1"

            if type == "weekly":
                sql += " AND YEARWEEK(date) = YEARWEEK(CURRENT_DATE())"
            elif type == "monthly":
                sql += " AND MONTH(date) = MONTH(CURRENT_DATE())"
            elif type == "annually":
                sql += " AND YEAR(date) = YEAR(CURRENT_DATE())"
            if start_date != "":
                sql += " AND date >= '" + start_date + "'"
            if end_date != "":
                sql += " AND date <= '" + end_date + "'"

            sql += ";"
        expenses = self.expenses_model.get_all_expense(sql)

        if(expenses != ()):
            # Creating a DataFrame
            df = pd.DataFrame(expenses)

            # Grouping by category_id and summing the amount
            grouped_category = df.groupby('category_id')['amount'].sum().reset_index()
            grouped_dict_category = grouped_category.to_dict(orient='records')

        return render_template('report.html', expenses=expenses, search_type=type, search_start=start_date, search_end=end_date, grouped_category=grouped_dict_category)

    def get_receipt_data(self):
        if request.method == 'POST':
            # Handle file upload
            upload_handler = FileUploadHandler(request, self.app.config['UPLOAD_FOLDER'])
            filepath, error = upload_handler.handle_upload()

            if error:
                return redirect(request.url)  # Handle error by redirecting to the upload form

            # Process the image if the upload was successful
            receipt_reader = ReceiptReader(filepath)
            preprocessed_image = receipt_reader.preprocess_image()
            extracted_text = receipt_reader.extract_text_from_image(preprocessed_image)
            receipt_details = receipt_reader.parse_receipt_data(extracted_text)

            vendor = receipt_details['vendor']
            date = receipt_details['date']
            currency = receipt_details['currency']
            items = receipt_details['items']
            categorized_items = receipt_reader.categorize_items(items)

            category = receipt_reader.get_main_category(categorized_items)
            amount = receipt_reader.extract_total(extracted_text)
            description = "Scanned Receipt"
            receipt = 1
            self.expenses_model.add_expense(vendor, category, description, currency, amount, date, receipt)

            # Pass data to the template
            return render_template('results.html', items=items, total=amount)

            # Render the upload form for GET requests
        return render_template('upload_file.html',title='Receipt Expense')


    def get_bank_statement_data(self):
        if request.method == 'POST':
            upload_handler = FileUploadHandler(request, self.app.config['UPLOAD_FOLDER'])
            filepath, error = upload_handler.handle_upload()
            if error:
                return redirect(request.url)

            # Create an instance of BankStatementReader
            bank_reader = BankStatementReader(self.app.config['UPLOAD_FOLDER'])
            # Extract text from the uploaded bank statement
            bank_statement_data = bank_reader.extract_text_from_file(filepath)
            parsed_data = bank_reader.parse_bank_statement(bank_statement_data)

            # Logic to compare transactions with stored receipts in the database
            matched_receipts = self.compare_transactions(parsed_data['transactions'])  # Implement this function

            return render_template('results.html', parsed_data=parsed_data, matched_receipts=matched_receipts)

        return render_template('upload_file.html',title='Bank Statement Expense')

    def compare_transactions(self,transactions):
        """Implement logic to compare transactions with stored receipts."""

        receipts = self.expenses_model.get_all_expense()  # Adjust this according to your method

        matched_receipts = []
        for transaction in transactions:
            for receipt in receipts:
                if transaction['amount'] == receipt['amount'] and transaction['description'] in receipt['description']:
                    matched_receipts.append({'transaction': transaction, 'receipt': receipt})

        return matched_receipts