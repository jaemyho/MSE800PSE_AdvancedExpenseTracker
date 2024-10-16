from flask_mysqldb import MySQL

from sql_statement import *


class UserModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def add_user(self, username, password, first_name,last_name,email,contact_number, company_id, role_id):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(ADD_NEW_USER,
                           (username, password,first_name,last_name,email,contact_number, company_id, role_id))
            self.mysql.connection.commit()
        except Exception as e:
            self.mysql.connection.rollback()
            print(f"Error adding user: {e}")
        finally:
            cursor.close()

    def add_company_details(self, company_name):
        cursor = self.mysql.connection.cursor()
        try:
            query = ADD_COMPANY_DETAILS
            values = (company_name,)
            cursor.execute(query, values)
            self.mysql.connection.commit()
            company_id = cursor.lastrowid
            return company_id
        except Exception as e:
            self.mysql.connection.rollback()
            print(f"Error adding company: {e}")
        finally:
            cursor.close()

    def get_user_by_username(self, username):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(GET_USER_BY_USERNAME, (username,))
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()

    def get_user_by_username_or_email(self, username, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute(GET_USER_BY_USERNAME_OR_EMAIL, (username, email))
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()
