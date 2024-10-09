import re
import datetime
from sql_statement import *
import MySQLdb

class AuditlogModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def __get_script_type__(self,sql):
        #return the sql statement type
        sql = sql.strip().upper()
        if sql.startswith("INSERT"):
            return "INSERT"
        elif sql.startswith("UPDATE"):
            return "UPDATE"
        elif sql.startswith("DELETE"):
            return "DELETE"
        else:
            return "Unknown"

    def __get_script_table__(self,script):
        # Regular expressions for different SQL commands
        patterns = {
            'INSERT': r'INSERT\s+INTO\s+(\w+)',
            'UPDATE': r'UPDATE\s+(\w+)',
            'DELETE': r'DELETE\s+FROM\s+(\w+)'
        }
        for command, pattern in patterns.items():
            match = re.search(pattern, script, re.IGNORECASE)
            if match:
                return match.group(1)

        return ""
    def add_auditlog(self, funct, user, script, record):
        type = self.__get_script_type__(script)
        table = self.__get_script_table__(script)
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            cur = self.mysql.connection.cursor()
            values = (type, user, current_date, funct, table, script, record)
            cur.execute(ADD_AUDITLOG, values)
            self.mysql.connection.commit()
            cur.close()
        except MySQLdb.Error as e:
            print(f"Audit Log Class - add_auditlog Error: {e}")

    def get_all_auditlog(self, mysql_script= GET_ALL_AUDITLOG):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(mysql_script)
            self.mysql.connection.commit()
            auditlogs = cur.fetchall()
            cur.close()
            return auditlogs
        except Exception as e:
            print(f"Get All Auditlog Error : {e}")
            return ()
