from flask_mysqldb import MySQL
import MySQLdb

class DatabaseModel:
    def __init__(self, app):
        self.mysql = MySQL(app)

    def check_table_exists(self, table_name):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cur.fetchone()
            cur.close()
            return result is not None
        except MySQLdb.Error as e:
            print(f"Error checking table existence: {e}")
            return False

    def create_table(self, sql_script):
        """Create the table if it does not exist."""
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(sql_script)
            self.mysql.connection.commit()
            cur.close()
        except MySQLdb.Error as e:
            print(f"Error creating table: {e}")