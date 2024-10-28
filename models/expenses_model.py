import os
from sql_statement import *
from models.auditlog_model import AuditlogModel
import datetime
from flask import session

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
            user_id = session['user_id']
            company_id = session['company_id']
            category_id = category
            currency_id = currency
            insert_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cur = self.mysql.connection.cursor()
            values = (user_id, company_id, category_id, vendor, description, currency_id, amount, inp_date, insert_date,receipt)
            cur.execute(ADD_SINGLE_EXPENSE, values)
            self.mysql.connection.commit()
            cur.close()

            self.auditlog.add_auditlog("add_expense",ADD_SINGLE_EXPENSE % values, str(values))
        except Exception as e:
            print(f"Expenses Add Expense Error : {e}")

    def update_expense(self, expense_id, vendor, category, description, currency, amount, inp_date, previous_expense):
        try:
            values = (vendor, category, description, currency, amount, inp_date, expense_id)
            cur = self.mysql.connection.cursor()
            cur.execute(UPDATE_SINGLE_EXPENSE_BY_ID, values)
            self.mysql.connection.commit()
            cur.close()
            self.auditlog.add_auditlog("update_expense", UPDATE_SINGLE_EXPENSE_BY_ID % values, str(previous_expense))
        except Exception as e:
            print(f"Expenses Update Expense Error : {e}")

    def delete_expense(self, expense_id,expense_details):
        try:
            values = (expense_id,)
            cur = self.mysql.connection.cursor()
            cur.execute(DELETE_SINGLE_EXPENSE_BY_ID, values)
            self.mysql.connection.commit()
            cur.close()
            self.auditlog.add_auditlog("delete_expense", DELETE_SINGLE_EXPENSE_BY_ID % values, str(expense_details))
        except Exception as e:
            print(f"Expenses Delete Expense Error : {e}")

    def get_all_expense(self,mysql_script = GET_ALL_EXPENSES):
        try:
            cur = self.mysql.connection.cursor()
            values =(session['company_id'],)
            cur.execute(mysql_script,values)
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
            values = (expense_id, session['company_id'])
            cur.execute(GET_EXPENSE_BY_ID, values)
            self.mysql.connection.commit()
            expense = cur.fetchone()
            cur.close()
            return expense
        except Exception as e:
            print(f"Get Expense by Id Error : {e}")
            return ()

    def get_total_expenses_amount(self , filter_script = ""):
        try:
            cur = self.mysql.connection.cursor()
            script = GET_TOTAL_EXPENSES + filter_script
            value = (session['company_id'],)
            cur.execute(script, value)
            self.mysql.connection.commit()
            total_expense = cur.fetchone()
            cur.close()
            return total_expense["total_expense"] if total_expense and total_expense["total_expense"] != "" else 0
        except Exception as e:
            print(f"Get Total Expenses Error : {e}")
            return 0

    def get_total_expenses_records(self, filter_script = ""):
        try:
            cur = self.mysql.connection.cursor()
            script = GET_TOTAL_EXPENSE_RECORDS + filter_script
            value = (session['company_id'],)
            cur.execute(script, value)
            self.mysql.connection.commit()
            total_records = cur.fetchone()
            cur.close()
            return total_records["total_records"] if total_records and total_records["total_records"] != "" else 0

        except Exception as e:
            print(f"Get Total Expenses Record Error : {e}")
            return 0

    def get_highest_expense_record(self, filter_script = ""):
        try:
            cur = self.mysql.connection.cursor()
            script = GET_HIGHEST_EXPENSE_RECORD + filter_script + ORDER_BY_AMOUNT + LIMIT_ONE
            value = (session['company_id'],)
            cur.execute(script, value)
            self.mysql.connection.commit()
            highest_expense = cur.fetchone()
            cur.close()
            return highest_expense
        except Exception as e:
            print(f"Get Highest Expense Record Error : {e}")
            return ()

    def get_today_total_expenses(self):
        try:
            cur = self.mysql.connection.cursor()
            value = (session['company_id'],)
            cur.execute(GET_TODAY_TOTAL_EXPENSES, value)
            self.mysql.connection.commit()
            today_expense = cur.fetchone()
            cur.close()
            return today_expense["total_amount"] if today_expense and today_expense["total_amount"] != "" else 0
        except Exception as e:
            print(f"Get Today Total Expense Error : {e}")
            return 0

    def get_yesterday_total_expenses(self):
        try:
            cur = self.mysql.connection.cursor()
            value = (session['company_id'],)
            cur.execute(GET_YESTERDAY_TOTAL_EXPENSES, value)
            self.mysql.connection.commit()
            yesterday_expense = cur.fetchone()
            cur.close()
            return yesterday_expense["total_amount"] if yesterday_expense and yesterday_expense["total_amount"] != "" else 0
        except Exception as e:
            print(f"Get Yesterday Total Expense Error : {e}")
            return 0

    def get_total_expense_group_date(self, filter_script = ""):
        try:
            cur = self.mysql.connection.cursor()
            script = GET_TOTAL_EXPENSE_GROUP_DATE + filter_script + GROUP_BY_DATE
            value = (session['company_id'],)
            cur.execute(script, value)
            self.mysql.connection.commit()
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            print(f"Get Total Expense Group By Date Error : {e}")
            return ()

    def get_total_expense_group_category(self, filter_script = ""):
        try:
            cur = self.mysql.connection.cursor()
            script = GET_EXPENSE_GROUP_BY_CATEGORY + filter_script + GROUP_BY_CAT_CATEGORY
            value = (session['company_id'],)
            cur.execute(script, value)
            self.mysql.connection.commit()
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            print(f"Get Total Expense Group By Category Error : {e}")
            return ()

    def get_daily_total_expense(self, filter_script = ""):
        try:
            cur = self.mysql.connection.cursor()
            script = GET_DAILY_TOTAL_EXPENSE + filter_script + GROUP_BY_DATE + ORDER_BY_DATE
            value = (session['company_id'],)
            cur.execute(script, value)
            self.mysql.connection.commit()
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            print(f"Get Daily Total Expense Group By Date Error : {e}")
            return ()

    def get_total_expenses_from_bank_statement_by_start_and_end_date(self,start_date,end_date):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(GET_TOTAL_EXPENSES_BY_START_DATE_AND_END_DATE, (start_date,end_date))
            self.mysql.connection.commit()
            expenses = cur.fetchall()
            cur.close()
            return expenses
        except Exception as e:
            print(f"Get All Expense Error : {e}")
            return ()