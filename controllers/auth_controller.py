from flask import render_template, request, redirect, url_for, flash, session
from models.user_model import UserModel
import bcrypt
from config import Config

class AuthController:
    def __init__(self, mysql, app):
        self.mysql = mysql
        self.app = app
        self.app.secret_key = Config.SECRET_KEY
        self.user_model = UserModel(mysql)

    def register(self):
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            company_name = request.form['company_name']
            contact_number = request.form['contact_number']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Validate that passwords match
            if password != confirm_password:
                flash("Passwords do not match", "danger")
                return redirect(url_for('register'))

            # Hash the password using bcrypt
            hashed_password = hash_password(password)

            # Check if the user already exists
            existing_user = self.user_model.get_user_by_username_or_email(username, email)
            if existing_user:
                flash("Username or email already exists", "danger")
                return redirect(url_for('register'))

            company_id = self.user_model.add_company_details(company_name)

            # Register the user
            self.user_model.add_user(
                username, hashed_password, first_name, last_name, email, contact_number, company_id
            )

            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))

        return render_template('register.html')

    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password'].strip()

            # Fetch user from the database
            user = self.user_model.get_user_by_username(username)
            if user and verify_password(user['password'], password):
                # Set user session
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['logged_in'] = True
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))  # Redirect to the dashboard or main page
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))

        return render_template('login.html')

    def logout(self):
        # Clear the session
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('logged_in', None)
        flash('You have been logged out', 'success')
        return redirect(url_for('login'))  # Redirect to the home page after logout

    def check_login(self):
        """Check if the user is logged in; redirect to login if not."""
        if not session.get('logged_in'):
            flash("You must be logged in to access this page", "warning")
            return redirect(url_for('login'))  # Redirect to login if not logged in
        else:
            print("logged in user", session.get('user_id'))
        return None

# Helper functions
def hash_password(password):
    # Generate a salt and hash the password with bcrypt
    salt = bcrypt.gensalt()  # Optionally, you can specify a log_rounds parameter
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Convert to string for storage

def verify_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
