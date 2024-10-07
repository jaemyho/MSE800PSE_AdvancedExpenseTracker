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
  PRIMARY KEY (`id`));
"""


CREATE_DB = "CREATE DATABASE IF NOT EXISTS"
DEFAULT_DB_NAME = "JaemyWeb"
AUDITLOG_TABLE = "AET_auditlog"
EXPENSE_TABLE = "AET_expense"
USER_TABLE = "AET_Users"

#SELECT SCRIPT
GET_ALL_EXPENSES = f"SELECT * FROM {EXPENSE_TABLE};"

#INSERT SCRIPT
ADD_AUDITLOG = f"INSERT INTO {AUDITLOG_TABLE} (type, user, insert_date, function_name, table_name, sql_statement) VALUES (%s, %s, %s, %s, %s, %s)"
ADD_SINGLE_EXPENSE = f"INSERT INTO {EXPENSE_TABLE} (user_id, company_id, category_id, vendor, description, currency_id, amount, date, insert_date,receipt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

#UPDATE SCRIPT


#DELET SCRIPT