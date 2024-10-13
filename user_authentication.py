from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, session
from models.user_model import UserModel

class UserAuthentication:
    def __init__(self, mysql):
        self.mysql = mysql

    def register(self, username, email, password, confirm_password):
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return False

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Initialize UserModel
        user_model = UserModel(self.mysql)

        # Check if the user already exists
        existing_user = user_model.get_user_by_username_or_email(username, email)
        if existing_user:
            flash("Username or email already exists", "danger")
            return False

        # Register the user
        user_model.add_user(username, email, hashed_password)
        flash("Registration successful! Please login.", "success")
        return True

    def login(self, username, password):
        # Initialize UserModel
        user_model = UserModel(self.mysql)

        # Fetch user from the database
        user = user_model.get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            # Set user session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return True
        else:
            flash('Invalid username or password', 'danger')
            return False

    def logout(self):
        # Clear the session
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('logged_in', None)
        flash('You have been logged out', 'success')
