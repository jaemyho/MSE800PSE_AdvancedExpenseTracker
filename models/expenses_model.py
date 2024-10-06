import os

from flask_mysqldb import MySQL
from sql_statement import *
from auditlog import auditlog
from receipt_reader import ReceiptReader
import datetime

class ExpensesModel:
    def __init__(self, app):
        self.mysql = MySQL(app)
        # self.auditlog = auditlog(app)
        self.receipt_reader = ReceiptReader
        self.upload_folder = app.config['UPLOAD_FOLDER']
        self.create_upload_folder()

    def create_upload_folder(self):
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def add_expense(self,vendor, category, description, currency, amount, inp_date,receipt):
        try:
            user_id = 1 #dummy data
            company_id = 1 #dummy data
            category_id = 1 #dummy data
            currency_id = 1 #dummy data
            insert_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cur = self.mysql.connection.cursor()
            values = (user_id, company_id, category_id, vendor, description, currency_id, amount, inp_date, insert_date,receipt)
            cur.execute(ADD_SINGLE_EXPENSE, values)
            self.mysql.connection.commit()
            cur.close()

            # self.auditlog.add_auditlog("add_expense","User",ADD_SINGLE_EXPENSE % values) #dummy data
        except Exception as e:
            print(f"Expenses Add Expense Error : {e}")

    def get_all_expense(self):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(GET_ALL_EXPENSES)
            self.mysql.connection.commit()
            expenses = cur.fetchall()
            cur.close()
            return expenses
        except Exception as e:
            print(f"Get All Expense Error : {e}")
            return ()
