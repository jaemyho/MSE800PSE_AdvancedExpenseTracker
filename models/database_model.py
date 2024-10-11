import MySQLdb

class DatabaseModel:
    def __init__(self, mysql):
        self.mysql = mysql

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

    def run_sql_script(self, sql_script):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(sql_script)
            self.mysql.connection.commit()
            cur.close()
        except MySQLdb.Error as e:
            print(f"Error database model - run sql script: {e}")

    def check_data_exists(self, table_name):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(f"SELECT * FROM {table_name}")
            result = cur.fetchone()
            cur.close()
            return result is not None
        except MySQLdb.Error as e:
            print(f"Error checking data existence: {e}")
            return False