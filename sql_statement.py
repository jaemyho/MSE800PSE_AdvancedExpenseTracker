CREATE_AUDITLOG_TABLE = """
CREATE TABLE IF NOT EXISTS `expensetracker`.`auditlog` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `insert_date` DATETIME NOT NULL,
  `function_name` VARCHAR(45) NOT NULL,
  `table_name` VARCHAR(45) NOT NULL,
  `sql_statement` VARCHAR(300) NOT NULL,
  PRIMARY KEY (`id`));
"""


CREATE_DB = "CREATE DATABASE IF NOT EXISTS"
DEFAULT_DB_NAME = "expensetracker"
AUDITLOG_TABLE = "auditlog"

#SELECT SCRIPT



#INSERT SCRIPT
ADD_AUDITLOG = f"INSERT INTO {AUDITLOG_TABLE} (type, user, insert_date, function_name, table_name, sql_statement) VALUES (%s, %s, %s, %s, %s, %s)"

#UPDATE SCRIPT


#DELET SCRIPT