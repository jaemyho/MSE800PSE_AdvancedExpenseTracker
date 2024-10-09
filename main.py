#Testing MVC Flask
from flask import Flask
from flask_mysqldb import MySQL
from config import Config
from controllers.expenses_controller import ExpenseController
from controllers.database_controller import DatabaseController
from controllers.auditlog_controller import AuditlogController

app = Flask(__name__, template_folder='views')  # Change the template folder to 'views'

# Configure MySQL
app.config.from_object(Config)
mysql = MySQL(app)

# Initialize the Controllers
expense_controller = ExpenseController(mysql,app)
database_controller = DatabaseController(mysql)
auditlog_controller = AuditlogController(mysql)

# Routes
@app.route('/')
def index():
    return expense_controller.index()
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    return expense_controller.add_expense()

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    return expense_controller.edit_expense(expense_id)

@app.route('/delete_expense/<int:expense_id>', methods=['GET', 'POST'])
def delete_expense(expense_id):
    return expense_controller.delete_expense(expense_id)

@app.route('/expenses/scan_file', methods=['GET', 'POST'])
def upload_file():
    return expense_controller.get_receipt_data()

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
