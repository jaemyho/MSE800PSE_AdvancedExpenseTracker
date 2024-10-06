#Testing MVC Flask
from flask import Flask
from config import Config
from controllers.expenses_controller import ExpenseController
from controllers.database_controller import DatabaseController

app = Flask(__name__, template_folder='views')  # Change the template folder to 'views'

# Configure MySQL
app.config.from_object(Config)
app.app_context().push()

# Initialize the Controllers
expense_controller = ExpenseController(app)
database_controller = DatabaseController(app)
# Routes
@app.route('/')
def index():
    return expense_controller.index()
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    return expense_controller.add_expense()

@app.route('/expenses/scan_file', methods=['GET', 'POST'])
def upload_file():
    return expense_controller.get_receipt_total()

@app.route('/report')
def report():
    return expense_controller.view_expense()

# Run the application
if __name__ == '__main__':
    # Check the database connection and table before starting the app
    database_controller.check_database_and_table()
    app.run(debug=True)
