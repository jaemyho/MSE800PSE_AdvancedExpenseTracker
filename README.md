# MSE800 Professional Software Engineering
Yoobee College MSE800 PSE Object-Oriented Programming Assignment

## Introduction
This project is a Python-based advanced expense tracker application designed to help users manage their expenses effectively. The project includes features for adding, editing, and viewing expenses by category, integrating with a MySQL database, and leveraging an MVC pattern with Flask.

## Developers from Yoobee College 2407-YCCIA-MSE - A
1. Jaemy Ho Seng Han (270402404)
2. Achini Wickramasinghe (270515598)
3. Resindu Navoda (270459868)

## Requirements
- Python 3.12
- MySQL Server (Modify config.py)
- Other dependencies listed in `requirements.txt`

## Configurations
1. **Database Configuration**:
 - Currently Database is connected to GoDaddy remove server MySQL database. (Yoobee College Education Wifi block the connection string, therefore mobile data is required to connect to the database)
 - Update the database configuration in `config.py` (or wherever your database configuration is stored).
   - Example:
     ```python
     DATABASE_CONFIG = {
         'host': 'localhost',
         'user': 'your_username',
         'password': 'your_password',
         'database': 'expense_tracker_db'
     }

## Files:
```plaintext
.

├─── .venv                     # virtual environment

├─── controllers               # controller layer
│    ├─── auditlog_controller.py    # handles audit log functions
│    ├─── auth_controller.py        # handles authentication functions
│    ├─── category_controller.py    # manages expense categories
│    ├─── currency_controller.py    # manages currency-related functions
│    ├─── database_controller.py    # manages database functions
│    ├─── expenses_controller.py    # handles expense functions
│    └─── user_controller.py        # manages user-related functions

├─── models                    # model layer
│    ├─── auditlog_model.py         # audit log data model
│    ├─── category_model.py         # category data model
│    ├─── currency_model.py         # currency data model
│    ├─── database_model.py         # database interaction model
│    ├─── expenses_model.py         # expenses data model
│    └─── user_model.py             # user data model

├─── output                    # output files (generated exe file)

├─── static                    # static files for the frontend
│    └─── style.css                 # stylesheet for the application

├─── uploads                   # directory to store file uploads (receipts and bank statement)

├─── views                     # HTML templates for the frontend
│    ├─── auditlog.html             # audit log view
│    ├─── base.html                 # base layout template
│    ├─── dashboard.html            # dashboard view
│    ├─── expense.html              # add/edit/delete expenses view
│    ├─── login.html                # login page view
│    ├─── register.html             # registration page view
│    ├─── report.html               # expense report page view
│    └─── upload_file.html          # upload file view

├─── bank_statement_reader.py   # processes bank statements
├─── config.py                  # database connection strings
├─── file_upload_handler.py     # handles file uploads and validation
├─── LICENSE.txt                # MIT License file
├─── main.py                    # main application entry point
├─── README.md                  # project documentation
├─── receipt_reader.py          # processes receipt data
├─── requirements.txt           # list of project dependencies
└─── sql_statement.py           # SQL statements for database operations
```

## MIT License
MIT License

Copyright (c) 2024 jaemyho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Git
https://github.com/jaemyho/MSE800PSE_AdvancedExpenseTracker.git