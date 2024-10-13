from flask_mysqldb import MySQL

class UserModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def add_user(self, username, password,first_name,last_name,email,contact_number):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO AET_users (username, password,first_name,last_name,email,contact_number) VALUES (%s, %s, %s,%s, %s, %s)",
                           (username, password,first_name,last_name,email,contact_number))
            self.mysql.connection.commit()
        except Exception as e:
            self.mysql.connection.rollback()
            print(f"Error adding user: {e}")
        finally:
            cursor.close()

    def get_user_by_username(self, username):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM AET_users WHERE username = %s", (username,))
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()

    def get_user_by_username_or_email(self, username, email):
        cursor = self.mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM AET_users WHERE username = %s OR email = %s", (username, email))
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()
