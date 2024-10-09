CREATE_AUDITLOG_TABLE = """
CREATE TABLE IF NOT EXISTS `AET_auditlog` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `insert_date` DATETIME NOT NULL,
  `function_name` VARCHAR(45) NOT NULL,
  `table_name` VARCHAR(45) NOT NULL,
  `sql_statement` VARCHAR(300) NOT NULL,
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
  `currency` INT NOT NULL,
  `expenditure_amount` FLOAT NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `insert_date` DATETIME NOT NULL,
  PRIMARY KEY (`id`));
"""

CREATE_DB = "CREATE DATABASE IF NOT EXISTS"
DEFAULT_DB_NAME = "JaemyWeb"
AUDITLOG_TABLE = "AET_auditlog"
EXPENSE_TABLE = "AET_expense"
USER_TABLE = "AET_Users"

#SELECT SCRIPT
GET_ALL_EXPENSES = f"SELECT * FROM {EXPENSE_TABLE};"
GET_EXPENSE_BY_ID = f"SELECT * FROM {EXPENSE_TABLE} WHERE id = %s;"

#INSERT SCRIPT
ADD_AUDITLOG = f"INSERT INTO {AUDITLOG_TABLE} (type, user, insert_date, function_name, table_name, sql_statement) VALUES (%s, %s, %s, %s, %s, %s)"
ADD_SINGLE_EXPENSE = f"INSERT INTO {EXPENSE_TABLE} (user_id, company_id, category_id, vendor, description, currency_id, amount, date, insert_date,receipt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

#UPDATE SCRIPT
UPDATE_SINGLE_EXPENSE_BY_ID = f"UPDATE {EXPENSE_TABLE} SET vendor = %s, category_id = %s, description = %s, currency_id = %s, amount = %s, date = %s WHERE id = %s;"

#DELET SCRIPT
DELETE_SINGLE_EXPENSE_BY_ID = f"DELETE FROM {EXPENSE_TABLE} WHERE id = %s;"