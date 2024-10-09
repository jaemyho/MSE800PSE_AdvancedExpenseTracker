import os
from sql_statement import *
from models.auditlog_model import AuditlogModel
import datetime

class ExpensesModel:
    def __init__(self, mysql,app):
        self.mysql = mysql
        self.auditlog = AuditlogModel(mysql)
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

            self.auditlog.add_auditlog("add_expense","User",ADD_SINGLE_EXPENSE % values, str(values)) #dummy data
        except Exception as e:
            print(f"Expenses Add Expense Error : {e}")

    def update_expense(self, expense_id, vendor, category, description, currency, amount, inp_date, previous_expense):
        try:
            currency = 1 #dummy data replace with currency id
            values = (vendor, category, description, currency, amount, inp_date, expense_id)
            cur = self.mysql.connection.cursor()
            cur.execute(UPDATE_SINGLE_EXPENSE_BY_ID, values)
            self.mysql.connection.commit()
            cur.close()
            self.auditlog.add_auditlog("update_expense", "User", UPDATE_SINGLE_EXPENSE_BY_ID % values, str(previous_expense))  # dummy data
        except Exception as e:
            print(f"Expenses Update Expense Error : {e}")

    def delete_expense(self, expense_id,expense_details):
        try:
            values = (expense_id,)
            cur = self.mysql.connection.cursor()
            cur.execute(DELETE_SINGLE_EXPENSE_BY_ID, values)
            self.mysql.connection.commit()
            cur.close()
            self.auditlog.add_auditlog("delete_expense", "User", DELETE_SINGLE_EXPENSE_BY_ID % values, str(expense_details))  # dummy data
        except Exception as e:
            print(f"Expenses Delete Expense Error : {e}")

    def get_all_expense(self,mysql_script = GET_ALL_EXPENSES):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(mysql_script)
            self.mysql.connection.commit()
            expenses = cur.fetchall()
            cur.close()
            return expenses
        except Exception as e:
            print(f"Get All Expense Error : {e}")
            return ()

    def get_expense_by_id(self,expense_id):
        try:
            cur = self.mysql.connection.cursor()
            values = (expense_id,)
            cur.execute(GET_EXPENSE_BY_ID, values)
            self.mysql.connection.commit()
            expense = cur.fetchone()
            cur.close()
            return expense
        except Exception as e:
            print(f"Get Expense by Id Error : {e}")
            return ()
