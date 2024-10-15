CREATE_AUDITLOG_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_auditlog` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `company_id` VARCHAR(45) NOT NULL,
  `insert_date` DATETIME NOT NULL,
  `function_name` VARCHAR(45) NOT NULL,
  `table_name` VARCHAR(45) NOT NULL,
  `sql_statement` VARCHAR(300) NOT NULL,
  `record` VARCHAR(300) NOT NULL,
  PRIMARY KEY (`id`));
"""

CREATE_EXPENSE_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_expense` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `company_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  `vendor` VARCHAR(45) NULL,
  `description` VARCHAR(45) NOT NULL,
  `currency_id` INT NOT NULL,
  `amount` FLOAT NOT NULL,
  `bank_statement` TINYINT NOT NULL DEFAULT 0,
  `date` DATE NOT NULL,
  `insert_date` DATETIME NOT NULL,
   `receipt`  TINYINT(4) DEFAULT 0 NOT NULL ,
    PRIMARY KEY (`id`));
"""

CREATE_BANK_STATEMENT_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_bank_statement_info` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `company_id` INT NOT NULL,
  `bank_name` VARCHAR(45) NULL,
  `customer_first_name` VARCHAR(45) NULL,
  `customer_last_name` VARCHAR(45) NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `currency` INT NOT NULL,
  `expenditure_amount` FLOAT NOT NULL,
  `insert_date` DATETIME NOT NULL,
  PRIMARY KEY (`id`));
"""


CREATE_USER_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `company_id` VARCHAR(45) NOT NULL,
  `role_id` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `contact_number` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));"""

CREATE_ROLES_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `role` VARCHAR(45) NOT NULL,
  `role_description` VARCHAR(100) NULL,
  PRIMARY KEY (`id`));
"""

CREATE_COMPANY_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_company` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_name` VARCHAR(45) NOT NULL,
  `industry` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `default_currency_id` INT NULL,
  PRIMARY KEY (`id`));
"""

CREATE_CURRENCY_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_currency` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `symbol` VARCHAR(45) NOT NULL,
  `exchange_rate` FLOAT NULL,
  `country` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));
"""

CREATE_CATEGORY_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));
"""

PREINESRT_CURRENCY_DATA = """
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('1', 'NZD', 'New Zealand Dollar', 'NZ$', '1', 'New Zealand');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('2', 'USD', 'United Statae Dollar', '$', '0.61', 'United States');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('3', 'EUR', 'Euro', '€', '0.56', 'Eurozone countries');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('4', 'JPY', 'Japanese Yen', '¥', '90.56', 'Japan');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('5', 'GBP', 'British Pound', '£', '0.46', 'United Kingdom');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('6', 'AUD', 'Australian Dollar', 'A$', '0.9', 'Australia');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('7', 'CAD', 'Canadian Dollar', 'C$', '0.83', 'Canada');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('8', 'CNY', '	Chinese Yuan', '	¥', '4.3', 'China');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('9', 'KRW', 'South Korean Won', '₩', '820.5', 'South Korea');
INSERT INTO `AET_currency` (`id`, `code`, `name`, `symbol`, `exchange_rate`, `country`) VALUES ('10', 'MYR', 'Malaysian Ringgit', 'RM', '2.6', 'Malaysia');
"""

PREINSERT_CATEGORY_DATA = """
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Food', 'Food');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Groceries', 'Groceries');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Entertainment', 'Entertainment');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Subscriptions', 'Subscriptions');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Rental', 'Rents');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Tax', 'Taxations');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Insurance', 'Insurance');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Medical', 'Medical  Expenses');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Education', 'Education');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Investments', 'Investment');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Transportation', 'Transportation');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Accomodation', 'Accomodation');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Clothings', 'Clothings');
INSERT INTO `AET_categories` (`category`, `description`) VALUES ('Events', 'Events');
"""

PREINSERT_ROLES_DATA = """
INSERT INTO `AET_roles` (`role`, `role_description`) VALUES ('System Admin', 'System Administrator');
INSERT INTO `AET_roles` (`role`, `role_description`) VALUES ('Owner', 'Company Owner');
INSERT INTO `AET_roles` (`role`, `role_description`) VALUES ('Admin', 'Company Administrator');
INSERT INTO `AET_roles` (`role`, `role_description`) VALUES ('Accountant', 'Company Accountant');
INSERT INTO `AET_roles` (`role`, `role_description`) VALUES ('User', 'Company User');
INSERT INTO `AET_roles` (`role`, `role_description`) VALUES ('Viewer', 'Viewer');
"""

PREINSERT_ADMIN_ACCOUNT = """
INSERT INTO `AET_users` (`username`, `password`, `company_id`, `role_id`, `first_name`, `last_name`, `email`, `contact_number`) VALUES ('admin', 'abc123', '0', '1', 'Admin', 'Admin', ' ', ' ');
"""

CREATE_DB = "CREATE DATABASE IF NOT EXISTS"
DEFAULT_DB_NAME = "JaemyWeb"
AUDITLOG_TABLE = "AET_auditlog"
EXPENSE_TABLE = "AET_expense"
USER_TABLE = "AET_users"
ROLES_TABLE = "AET_roles"
COMPANY_TABLE = "AET_company"
CURRENCY_TABLE = "AET_currency"
CATEGORY_TABLE = "AET_categories"
BANK_STATEMENT_TABLE = "AET_bank_statement_info"
EXPENSE_FILTER_THIS_WEEK = " AND YEARWEEK(date, 1) = YEARWEEK(CURDATE(), 1)"
EXPENSE_FILTER_THIS_MONTH = " AND YEAR(date) = YEAR(CURDATE()) AND MONTH(date) = MONTH(CURDATE())"
EXPENSE_FILTER_THIS_YEAR = " AND YEAR(date) = YEAR(CURDATE())"
GROUP_BY_DATE = " GROUP BY DATE(date)"
GROUP_BY_CAT_CATEGORY = " GROUP BY cat.category"
ORDER_BY_DATE = " ORDER BY DATE(date)"
ORDER_BY_AMOUNT = " ORDER BY exp.amount DESC"
LIMIT_ONE = " LIMIT 1"
GET_DAILY_TOTAL_EXPENSE = (f"SELECT DATE(date) AS day, SUM(amount) AS total_amount FROM {EXPENSE_TABLE} "
                           f"WHERE company_id = %s ")

#SELECT SCRIPT
GET_ALL_EXPENSES = (f"SELECT exp.*, usr.username as user, curr.code as currency, cat.category as category FROM {EXPENSE_TABLE} as exp "
                    f"LEFT JOIN {USER_TABLE} as usr ON exp.user_id = usr.id "
                    f"LEFT JOIN {CURRENCY_TABLE} as curr ON exp.currency_id = curr.id "
                    f"LEFT JOIN {CATEGORY_TABLE} as cat ON exp.category_id = cat.id WHERE exp.company_id = %s;")
GET_EXPENSE_BY_ID = f"SELECT * FROM {EXPENSE_TABLE} WHERE id = %s and company_id = %s;"
GET_ALL_AUDITLOG = f"SELECT * FROM {AUDITLOG_TABLE} WHERE company_id = %s;"
GET_ALL_CURRENCIES = f"SELECT * FROM {CURRENCY_TABLE};"
GET_ALL_CATEGORIES = f"SELECT * FROM {CATEGORY_TABLE};"
GET_TOTAL_EXPENSES = f"SELECT sum(amount) AS total_expense FROM {EXPENSE_TABLE} WHERE company_id = %s"
GET_TOTAL_EXPENSE_RECORDS = f"SELECT COUNT(*) AS total_records FROM {EXPENSE_TABLE} WHERE company_id = %s"
GET_HIGHEST_EXPENSE_RECORD = f"SELECT exp.amount, cat.category FROM {EXPENSE_TABLE} AS exp LEFT JOIN {CATEGORY_TABLE} AS cat ON exp.category_id = cat.id WHERE exp.company_id = %s"
GET_TODAY_TOTAL_EXPENSES = f"SELECT SUM(amount) AS total_amount FROM {EXPENSE_TABLE} WHERE company_id = %s AND DATE(date) = CURDATE();"
GET_YESTERDAY_TOTAL_EXPENSES = f"SELECT SUM(amount) AS total_amount FROM {EXPENSE_TABLE} WHERE company_id = %s AND DATE(date) = CURDATE() - INTERVAL 1 DAY;"
GET_TOTAL_EXPENSE_BY_DAYS = f"SELECT DATE(date) as date, SUM(amount) as amount FROM {EXPENSE_TABLE} WHERE company_id = %s "
GET_TOTAL_EXPENSE_GROUP_DATE = f"SELECT DATE(date) as date, SUM(amount) as amount FROM {EXPENSE_TABLE} WHERE company_id = %s "
GET_EXPENSE_GROUP_BY_CATEGORY = (f"SELECT cat.category, COALESCE(SUM(exp.amount), 0) AS amount "
                                 f"FROM {CATEGORY_TABLE} AS cat "
                                 f"LEFT JOIN {EXPENSE_TABLE} AS exp "
                                 f"ON exp.category_id = cat.id AND exp.company_id = %s ")
GET_USER_BY_USERNAME = f"SELECT * FROM AET_users WHERE username = %s"
GET_USER_BY_USERNAME_OR_EMAIL = f"SELECT * FROM AET_users WHERE username = %s OR email = %s"

#INSERT SCRIPT
ADD_NEW_USER = f"INSERT INTO AET_users (username, password,first_name,last_name,email,contact_number, company_id) VALUES (%s, %s, %s,%s, %s, %s, %s)"
ADD_AUDITLOG = f"INSERT INTO {AUDITLOG_TABLE} (type, user, company_id, insert_date, function_name, table_name, sql_statement, record) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
ADD_SINGLE_EXPENSE = f"INSERT INTO {EXPENSE_TABLE} (user_id, company_id, category_id, vendor, description, currency_id, amount, date, insert_date,receipt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
ADD_COMPANY_DETAILS = f"INSERT INTO AET_company (company_name) VALUES (%s)"
#UPDATE SCRIPT
UPDATE_SINGLE_EXPENSE_BY_ID = f"UPDATE {EXPENSE_TABLE} SET vendor = %s, category_id = %s, description = %s, currency_id = %s, amount = %s, date = %s WHERE id = %s;"

#DELET SCRIPT
DELETE_SINGLE_EXPENSE_BY_ID = f"DELETE FROM {EXPENSE_TABLE} WHERE id = %s;"