from flask_mysqldb import MySQL
from sql_statement import *

class UserModel:
    def __init__(self, app):
        self.mysql = MySQL(app)