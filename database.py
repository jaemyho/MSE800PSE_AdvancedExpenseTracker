import datetime
import configparser
import pymysql
#import mysql.connector
#from mysql.connector import cursor
from sql_statement import *

class Database:
    def __init__(self):
        self.config_filename = 'configfile.ini'
        self.connection = None #Hold the connection object
        self._init_database()

    def _init_database(self):
        config = self.load_config()
        self.connection = pymysql.connect(**config, autocommit=True)
        if self.connection:
            self._check_database_exist()
            self._check_tables_exist()
            self._preinsert_data()
            return True
        return False

    #Load database configurations
    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_filename)
        return {key:value for key, value in config['mysql'].items()}

    def save_config(self, config):
        config_parser = configparser.ConfigParser()
        config_parser['mysql'] = config
        with open(self.config_filename, 'w') as configfile:
            config_parser.write(configfile)

    #Database connection
    def create_connection_parser(self):
        config = self.load_config()
        self.connection = pymysql.connect(**config, autocommit=True)
        if self.connection:
            return self.connection.cursor()
        else:
            raise Exception()

    def _check_database_exist(self):
        config = self.load_config()
        if not config.get("database"):
            config['database'] = DEFAULT_DB_NAME
            self.save_config(config)

            cursor = self.create_connection_parser()
            cursor.execute(f"{CREATE_DB}{config['database']};")

    def _check_tables_exist(self):
        cursor = self.create_connection_parser()
        cursor.execute(CREATE_AUDITLOG_TABLE)

    def _preinsert_data(self):
        cursor = self.create_connection_parser()
