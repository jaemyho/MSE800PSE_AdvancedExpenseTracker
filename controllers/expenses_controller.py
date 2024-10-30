from datetime import datetime

from flask import render_template, request, redirect, url_for, session, flash
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
        self.expense_filter = "week"
        self.filters = {
            "all": "",
            "week": EXPENSE_FILTER_THIS_WEEK,
            "month": EXPENSE_FILTER_THIS_MONTH,
            "year": EXPENSE_FILTER_THIS_YEAR
        }

    #Home page
    def dashboard(self):
        if request.method == 'POST':
            self.expense_filter = request.form['search_type']

        filter_value = self.filters.get(self.expense_filter, "")

        total_expense_amount = self.expenses_model.get_total_expenses_amount(filter_value)
        total_expense_records = self.expenses_model.get_total_expenses_records(filter_value)
        temp_max_expense_record = self.expenses_model.get_highest_expense_record(filter_value)
        today_total_expense = self.expenses_model.get_today_total_expenses()
        yesteday_total_expense = self.expenses_model.get_yesterday_total_expenses()
        total_expense_group_date = self.expenses_model.get_total_expense_group_date(filter_value)
        total_expense_group_category = self.expenses_model.get_total_expense_group_category(filter_value)
        daily_total_expense_group_by_date = self.expenses_model.get_daily_total_expense(filter_value)

        for x in daily_total_expense_group_by_date:
            x['day'] = x['day'].strftime('%Y-%m-%d')

        max_expense_record = {
            'amount': 0,
            'category': "None"
        }
        if temp_max_expense_record != None:
            max_expense_record['amount'] = self.safe_round(temp_max_expense_record['amount'])
            max_expense_record['category'] = temp_max_expense_record['category']

        data = {
            'search_type': self.expense_filter,
            'total_expense': self.safe_round(total_expense_amount),
            'total_records': total_expense_records,
            'max_expense_record': max_expense_record,
            'today_total_expense': self.safe_round(today_total_expense),
            'yesterday_total_expense': self.safe_round(yesteday_total_expense),
            'total_expense_group_date': total_expense_group_date,
            'total_expense_group_category': total_expense_group_category,
            'daily_total_expense_group_by_date': daily_total_expense_group_by_date
        }
        return render_template('dashboard.html', **data)

    def safe_round(self, value):
        return round(value, 2) if value is not None else 0

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

        data = {
            'title' : 'Add Expense',
            'expense' : "",
            'currencies' : currencies,
            'categories' : categories
        }
        return render_template('expense.html', **data)

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

        data = {
            'title': 'Edit Expense',
            'expense': expense,
            'currencies': currencies,
            'categories': categories
        }
        return render_template('expense.html', **data)

    def delete_expense(self, expense_id):
        expense = self.expenses_model.get_expense_by_id(expense_id)
        currencies = self.currency_controller.get_all_currencies()
        categories = self.category_controller.get_all_categories()
        if request.method == 'POST':
            self.expenses_model.delete_expense(expense_id,expense)
            return redirect(url_for('report'))

        data = {
            'title': 'Delete Expense',
            'expense': expense,
            'currencies': currencies,
            'categories': categories
        }
        return render_template('expense.html', **data)

    def view_expense(self):
        sql = GET_ALL_EXPENSES
        type, start_date, end_date, grouped_dict_category = "", "", "", {}
        if request.method == 'POST':
            type = request.form['search_type']
            start_date = request.form['search_start']
            end_date = request.form['search_end']

            if type == "weekly":
                sql += EXPENSE_FILTER_THIS_WEEK
            elif type == "monthly":
                sql += EXPENSE_FILTER_THIS_MONTH
            elif type == "annually":
                sql += EXPENSE_FILTER_THIS_YEAR
            if start_date != "":
                sql += " AND date >= '" + start_date + "'"
            if end_date != "":
                sql += " AND date <= '" + end_date + "'"

        sql += ORDER_BY_DATE + " DESC"
        expenses = self.expenses_model.get_all_expense(sql)

        # Update bank_statement values
        for record in expenses:
            if record['bank_statement'] == 0:
                record['bank_statement'] = 'unmatched'
            elif record['bank_statement'] == 1:
                record['bank_statement'] = 'matched'

        if(expenses != ()):
            # Creating a DataFrame
            df = pd.DataFrame(expenses)

            # Grouping by category_id and summing the amount
            grouped_category = df.groupby('category')['amount'].sum().reset_index()
            grouped_dict_category = grouped_category.to_dict(orient='records')

        data = {
            'expenses' : expenses,
            'serach_type' : type,
            'search_start' : start_date,
            'search_end' : end_date,
            'grouped_dict_category' : grouped_dict_category
        }

        return render_template('report.html', **data)

    def get_receipt_data(self):
        currencies = self.currency_controller.get_all_currencies()
        categories = self.category_controller.get_all_categories()
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
            print("extracted_text", extracted_text)
            receipt_details = receipt_reader.parse_receipt_data(extracted_text)

            vendor = receipt_reader.extract_shop_name(extracted_text)
            print("vendor", vendor)
            # converting date into the YYYY-MM-DD format
            date = receipt_details['date']  # initial 'MM/DD/YYYY' format
            print("date", date)

            currency = receipt_details['currency']
            items = receipt_details['items']
            print("items", items)
            categorized_items = receipt_reader.categorize_items(items)
            print("categorized_items", categorized_items)

            category = receipt_reader.get_category_from_receipt(extracted_text)
            category_id = self.expenses_model.get_category_id(category)
            print("category", category)
            print("category_id", category_id)
            amount = receipt_reader.extract_total(extracted_text)
            description = receipt_reader.extract_description(extracted_text)
            receipt_details['description'] = description
            print("description", description)
            receipt = 1
            # Pass data to the template
            return render_template('expense.html', title='Receipt Expense', items=items, total=amount,
                                   expense=receipt_details, currencies=currencies, categories=categories,category=category)
            flash("Uploaded successful!.", "success")

            # Render the upload form for GET requests
        return render_template('upload_file.html',title='Receipt Upload')

    def add_expenses_to_db(self):
        if request.method == 'POST':
            vendor = request.form['vendor']
            category = request.form['category']
            description = request.form['description']
            currency = request.form['currency']
            amount = request.form['amount']
            date = request.form['expense_date']
            receipt = 1  # Assuming you have a receipt ID or similar mechanism

            # Add the expense to the database
            self.expenses_model.add_expense(vendor, category, description, currency, amount, date, receipt)
            flash("Expense submitted successfully!", "success")

            # Redirect to a desired route after successful submission
            return redirect(url_for('upload_file'))  # Change to the route you want to go after submission

    def get_bank_statement_data(self):
        if request.method == 'POST':
            upload_handler = FileUploadHandler(request, self.app.config['UPLOAD_FOLDER'])
            filepath, error = upload_handler.handle_upload()
            if error:
                return redirect(request.url)

            # Create an instance of BankStatementReader
            bank_reader = BankStatementReader(self.app.config['UPLOAD_FOLDER'])
            # Extract text from the uploaded bank statement
            extracted_bank_statement_data = bank_reader.extract_text_from_file(filepath)
            parsed_bank_statement_transactions = bank_reader.extract_transactions(extracted_bank_statement_data)
            print("parsed_data", parsed_bank_statement_transactions)

            for transaction in parsed_bank_statement_transactions:
                print("transaction new", transaction['Date'])
                self.expenses_model.update_bank_statement_matched_status(transaction['Date'], transaction['Debit'])
                bank_statement_status = self.expenses_model.get_bank_statement_status_by_date_and_debit_amount(
                    transaction['Date'], transaction['Debit'])

                if bank_statement_status:
                    # Access the first element of the tuple
                    status_dict = bank_statement_status[0]
                    # Check the 'bank_statement' key
                    if 'bank_statement' in status_dict:
                        if status_dict['bank_statement'] == 1:
                            transaction['Status'] = "matched"
                        else:
                            transaction['Status'] = "unmatched"
                    else:
                        transaction['Status'] = "Status key not found"
                else:
                    transaction['Status'] = "Unmatched"

            print("final parsed_bank_statement_transactions", parsed_bank_statement_transactions)

            return render_template('upload_file.html', transactions=parsed_bank_statement_transactions)

        return render_template('upload_file.html', title='Bank Statement Expense')


