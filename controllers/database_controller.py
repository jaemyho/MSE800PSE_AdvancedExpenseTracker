from models.database_model import DatabaseModel
from sql_statement import *
import MySQLdb
class DatabaseController:
    def __init__(self, mysql):
        self.database_model = DatabaseModel(mysql)

    def check_database_and_table(self):
        """Check if the database connection works and if the 'users' table exists."""
        try:
            # Check if the table exists
            tables_to_create = {
                USER_TABLE: CREATE_USER_TABLE,
                EXPENSE_TABLE: CREATE_EXPENSE_TABLE,
                AUDITLOG_TABLE: CREATE_AUDITLOG_TABLE,
                ROLES_TABLE: CREATE_ROLES_TABLE,
                COMPANY_TABLE: CREATE_COMPANY_TABLE,
                CURRENCY_TABLE: CREATE_CURRENCY_TABLE,
                CATEGORY_TABLE: CREATE_CATEGORY_TABLE
            }

            for table_name, create_statement in tables_to_create.items():
                if not self.database_model.check_table_exists(table_name):
                    self.database_model.run_sql_script(create_statement)

            # Pre Insert Data
            table_to_insert = {
                USER_TABLE: PREINSERT_ADMIN_ACCOUNT,
                CURRENCY_TABLE: PREINESRT_CURRENCY_DATA,
                CATEGORY_TABLE: PREINSERT_CATEGORY_DATA,
                ROLES_TABLE: PREINSERT_ROLES_DATA
            }

            for table_name, insert_statement in table_to_insert.items():
                # Check if data already exists in the table
                if not self.database_model.check_data_exists(table_name):
                    # If data doesn't exist, execute the insert statement
                    for statement in insert_statement.split(';'):
                        statement = statement.strip()
                        if statement:
                            self.database_model.run_sql_script(statement)

        except MySQLdb.Error as e:
            print(f"Error checking database: {e}")
            exit(1)  # Exit the program if there is an issue