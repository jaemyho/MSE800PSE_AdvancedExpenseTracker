from flask import render_template, request, redirect, url_for
from models.database_model import DatabaseModel
from sql_statement import *
import MySQLdb
class DatabaseController:
    def __init__(self, app):
        self.database_model = DatabaseModel(app)

    def check_database_and_table(self):
        """Check if the database connection works and if the 'users' table exists."""
        try:
            # Check if the table exists
            # user table
            #if not self.database_model.check_table_exists(USER_TABLE):
                #self.database_model.create_table(USER_TABLE)
            # expenses table
            if not self.database_model.check_table_exists(EXPENSE_TABLE):
                self.database_model.create_table(CREATE_EXPENSE_TABLE)
            #auditlog table
            if not self.database_model.check_table_exists(AUDITLOG_TABLE):
                self.database_model.create_table(CREATE_AUDITLOG_TABLE)

        except MySQLdb.Error as e:
            print(f"Error checking database: {e}")
            exit(1)  # Exit the program if there is an issue