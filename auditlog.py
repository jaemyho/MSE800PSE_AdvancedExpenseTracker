import re
import datetime
import configparser
from database import Database
from sql_statement import *

db = Database()
class auditlog():
    def __init__(self):
        self.type = ""
        self.table = ""
        self.date = datetime.datetime.now()
        self.funct = ""
        self.user = ""
        self.script = ""

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
    def add_auditlog(self, funct, user, script):
        type = self.__get_script_type__(script)
        table = self.__get_script_table__(script)
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            cursor = db.create_connection_parser()
            values = (type, user, current_date, funct, table, script)
            cursor.execute(ADD_AUDITLOG, values)
        except configparser.Error as e:
            print(f"Audit Log Class - add_auditlog Error: {e}")

