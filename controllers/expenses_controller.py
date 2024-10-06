from flask import render_template, request, redirect, url_for
from models.expenses_model import ExpensesModel
from file_upload_handler import FileUploadHandler
from receipt_reader import ReceiptReader
import datetime
class ExpenseController:
    def __init__(self, app):
        self.app = app
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
            receipt = 0
            self.expenses_model.add_expense(vendor, category, description, currency, amount, date,receipt)
            return redirect(url_for('add_expense'))  # Redirect to the add user page after successful submission
        return render_template('add_expense.html')

    def view_expense(self):
        expenses = self.expenses_model.get_all_expense()
        print(expenses)
        #expenses = ({'id': 1, 'user_id': 1, 'company_id': 1, 'category_id': 1, 'vendor': 'KFC', 'description': 'Breakfaswt', 'currency_id': 1, 'amount': 30.0, 'bank_statement': 0, 'date': datetime.date(2024, 10, 4), 'insert_date': datetime.datetime(2024, 10, 4, 0, 0)}, {'id': 2, 'user_id': 1, 'company_id': 1, 'category_id': 1, 'vendor': 'KFC', 'description': 'Breakfast', 'currency_id': 1, 'amount': 30.0, 'bank_statement': 0, 'date': datetime.date(2024, 10, 4), 'insert_date': datetime.datetime(2024, 10, 4, 0, 0)})
        return render_template('index.html')
        #return render_template('report.html', expenses=expenses)

    def get_receipt_total(self):
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
            self.expenses_model.add_expense(vendor, category, description, currency, amount, date,receipt)

            # Pass data to the template
            return render_template('results.html', items=items, total=amount)

            # Render the upload form for GET requests
        return render_template('upload_file.html')