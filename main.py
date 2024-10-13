#Testing MVC Flask
from flask import Flask, session
from flask_mysqldb import MySQL
from config import Config
from controllers.auth_controller import AuthController
from controllers.expenses_controller import ExpenseController
from controllers.database_controller import DatabaseController
from controllers.auditlog_controller import AuditlogController
from controllers.auth_controller import AuthController

app = Flask(__name__, template_folder='views')  # Change the template folder to 'views'

# Configure MySQL
app.config.from_object(Config)
mysql = MySQL(app)

# Initialize the Controllers
expense_controller = ExpenseController(mysql,app)
database_controller = DatabaseController(mysql)
auditlog_controller = AuditlogController(mysql)
auth_controller = AuthController(mysql,app)

# Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    return auth_controller.register()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth_controller.login()

@app.route('/logout')
def logout():
    return auth_controller.logout()

@app.route('/dashboard', methods=['GET', 'POST'])
def index():
    return expense_controller.index()
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    # Check if the user is logged in
    redirect_response = auth_controller.check_login()
    if redirect_response:
        return redirect_response  # Redirect to login if not logged in

    # Proceed to add expense if logged in
    return expense_controller.add_expense()

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    return expense_controller.edit_expense(expense_id)

@app.route('/delete_expense/<int:expense_id>', methods=['GET', 'POST'])
def delete_expense(expense_id):
    return expense_controller.delete_expense(expense_id)

@app.route('/expenses/scan_file', methods=['GET', 'POST'])
def upload_file():
    redirect_response = auth_controller.check_login()
    if redirect_response:
        return redirect_response  # Redirect to login if not logged in

    return expense_controller.get_receipt_data()

@app.route('/expenses/upload_bank_statement', methods=['GET', 'POST'])
def upload_bank_statement():
    return expense_controller.get_bank_statement_data()

@app.route('/report', methods=['GET', 'POST'])
def report():
    return expense_controller.view_expense()

@app.route('/auditlogreport', methods=['GET', 'POST'])
def auditlogreport():
    return auditlog_controller.view_auditlog()

# Run the application
if __name__ == '__main__':
    # Check the database connection and table before starting the app
    with app.app_context():
        database_controller.check_database_and_table()
    app.run(debug=True)
