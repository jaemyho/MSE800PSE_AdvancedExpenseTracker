import re
import json
from datetime import datetime, date

from flask import render_template, request, redirect, url_for
from models.auditlog_model import AuditlogModel
from models.currency_model import CurrencyModel
from models.category_model import CategoryModel
from sql_statement import *

class AuditlogController:

    def __init__(self, mysql):
        self.auditlog = AuditlogModel(mysql)
        self.currencymodel = CurrencyModel(mysql)
        self.categorymodel = CategoryModel(mysql)
        self.all_currencies = None
        self.all_categories = None

    def view_auditlog(self):
        self.all_currencies = self.currencymodel.get_all_currencies()
        self.all_categories = self.categorymodel.get_all_categories()

        sql = GET_ALL_AUDITLOG
        type, duration, start_date, end_date = "insert", "", "", ""
        if request.method == 'POST':
            type = request.form['search_type']
            duration = request.form['search_duration']
            start_date = request.form['search_start']
            end_date = request.form['search_end']

        sql = self.auditlog_script_by_filter(sql, type, duration, start_date, end_date)
        auditlogs = self.auditlog.get_all_auditlog(sql)
        auditlogs_data = self.log_processing(type, auditlogs)

        auditlogs_data = {} if auditlogs_data is None else auditlogs_data
        data = {
            'auditlogs': auditlogs_data,
            'search_type': type,
            'search_duration': duration,
            'search_start': start_date,
            'search_end': end_date,
        }
        return render_template('auditlog.html', **data)


    def auditlog_script_by_filter(self, sql, type, duration, start_date, end_date):
        # search by types
        sql += " AND type = '" + type + "'"

        # search by durations
        if duration == "weekly":
            sql += " AND YEARWEEK(insert_date) = YEARWEEK(CURRENT_DATE())"
        elif duration == "monthly":
            sql += " AND MONTH(insert_date) = MONTH(CURRENT_DATE())"
        elif duration == "annually":
            sql += " AND YEAR(insert_date) = YEAR(CURRENT_DATE())"

        # search by start or end date
        if start_date != "":
            sql += " AND insert_date >= '" + start_date + "'"
        if end_date != "":
            sql += " AND insert_date <= '" + end_date + "'"

        return sql

    def log_processing(self, type, auditlogs):
        if type == 'insert':
            return self.process_insert_log_data(auditlogs)
        elif type == 'update':
            return self.process_update_log_data(auditlogs)
        elif type =='delete':
            return self.process_delete_log_data(auditlogs)

    def process_insert_log_data(self, auditlogs):
        for data in auditlogs:
            # Use regex to extract column names and values
            columns_match = re.search(r'\((.*?)\)', data['sql_statement'])
            values_match = re.search(r'VALUES \((.*?)\)', data['sql_statement'])

            if columns_match and values_match:
                columns = [col.strip() for col in columns_match.group(1).split(',')]
                values = [val.strip().strip("'") for val in values_match.group(1).split(',')]

                # Add columns and values to the entry
                data['columns'] = columns
                data['values'] = values

        return self.process_insert_log_data_table(auditlogs)


    def process_insert_log_data_table(self, auditlogs):
        records = []
        for entry in auditlogs:
            curreny_code = None
            category_name = None
            for currency in self.all_currencies:
                if str(currency['id']) == str(entry['record'].split(", ")[5].strip("'")):
                    curreny_code = currency['code']
            for category in self.all_categories:
                if str(category['id']) == str(entry['record'].split(", ")[2].strip("'")):
                    category_name = category['category']

            record_info = {
                'ID': entry['id'],
                'Type': entry['type'],
                'User': entry['username'],
                'Insert_Date': entry['insert_date'].strftime('%Y-%m-%d %H:%M:%S'),  # Formatting datetime
                'Expense_Date': entry['record'].split(", ")[7].strip("'"),  # Extracting from record
                'Category': category_name,
                'Vendor': entry['record'].split(", ")[3].strip("'"),
                'Description': entry['record'].split(", ")[4].strip("'"),
                'Currency': curreny_code,
                'Amount': entry['record'].split(", ")[6].strip("'"),
            }
            records.append(record_info)
        return records

    def process_update_log_data(self, auditlogs):
        record_infos = []
        for data in auditlogs:
            # Convert record JSON-like string to dictionary
            original_record = self.convert_record_to_dict(data['record'])

            # Find updated columns
            updated = self.find_updated_columns(data['sql_statement'], original_record)
            print(updated)
            # converting Category ID to Catergory and Currency_ID to currency, also forming col: before -> after
            updated_columns = {
                ('Category' if col == 'category_id' else 'Currency' if col == 'currency_id' else col):
                    f"{details['original']} -> {details['updated']}"
                for col, details in updated.items()
            }
            updated_columns_one_string = ', '.join([f"{key}: {value}" for key, value in updated_columns.items()])
            # Create the formatted output
            record_info = {
                'ID': data['id'],
                'Type': data['type'],
                'User': data['username'],
                'Insert_Date': data['insert_date'].strftime('%Y-%m-%d %H:%M:%S'),
                'Updated_Column': updated_columns_one_string
            }

            record_infos.append(record_info)

        return record_infos

    # Function to parse the SQL statement and identify changes
    def find_updated_columns(self, update_sql, original_record):
        changes = {}
        remove_clause = update_sql.split("SET")[1].split("WHERE")[0].strip()
        updated_data = remove_clause.split(',')

        for new_data in updated_data:
            field, new_value = new_data.strip().split('=')
            field = field.strip()
            new_value = new_value.strip()

            # Convert value types
            if new_value.isdigit():
                new_value = int(new_value)
            elif new_value.replace('.', '', 1).isdigit():
                new_value = float(new_value)
            elif new_value == 'NULL':
                new_value = None
            else:
                new_value = new_value.strip().replace("'", "")

            # Compare with original record to detect changes
            if field in original_record and original_record[field] != new_value:
                if field == "category_id":
                    # Retrieve category codes
                    ori_cat, new_cat = "", ""
                    for category in self.all_categories:  # Assuming categories mapping list
                        if str(category['id']) == str(original_record[field]):
                            ori_cat = category['category']
                        if str(category['id']) == str(new_value):
                            new_cat = category['category']
                    changes[field] = {"original": ori_cat, "updated": new_cat}
                elif field == "currency_id":
                    # Retrieve currency codes
                    ori_cur, new_cur = "", ""
                    for currency in self.all_currencies:
                        if str(currency['id']) == str(original_record[field]):
                            ori_cur = currency['code']
                        if str(currency['id']) == str(new_value):
                            new_cur = currency['code']
                    changes[field] = {"original": ori_cur, "updated": new_cur}
                else:
                    # General fields
                    changes[field] = {
                        "original": original_record[field],
                        "updated": new_value
                    }

        return changes

    def convert_record_to_dict(self, record_str):
        # Adjust for JSON compatibility and datetime representations
        record_str = record_str.replace("'", '"')
        record_str = re.sub(r'datetime\.date\((\d{4}), (\d{1,2}), (\d{1,2})\)', r'"\1-\2-\3"', record_str)
        record_str = re.sub(r'datetime\.datetime\((\d{4}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2})\)',
                            r'"\1-\2-\3 \4:\5:\6"', record_str)
        return json.loads(record_str)

    def process_delete_log_data(self, auditlogs):
        records = []
        for data in auditlogs:
            record_str = data['record']

            # Extract specific fields from the record
            currency_code, category_name = "", ""
            expense_date = self.extract_value_from_record(record_str, 'date')
            category_id_str = self.extract_value_from_record(record_str, 'category_id')
            vendor = self.extract_value_from_record(record_str, 'vendor')
            description = self.extract_value_from_record(record_str, 'description')
            currency_id_str = self.extract_value_from_record(record_str, 'currency_id')
            amount = self.extract_value_from_record(record_str, 'amount')

            for currency in self.all_currencies:
                if str(currency['id']) == str(currency_id_str):
                    currency_code = currency['code']
            for category in self.all_categories:
                if str(category['id']) == str(category_id_str):
                    category_name = category['category']

            # Creating the formatted record info
            record_info = {
                'ID': data['id'],
                'Type': data['type'],
                'User': data['username'],
                'Insert_Date': data['insert_date'].strftime('%Y-%m-%d %H:%M:%S'),
                'Expense_Date': expense_date,
                'Category': category_name,
                'Vendor': vendor,
                'Description': description,
                'Currency': currency_code,
                'Amount': amount
            }

            records.append(record_info)
        return records

    def extract_value_from_record(self, record, field_name):

        # If record is a string, parse it to a dictionary
        if isinstance(record, str):
            record = self.convert_record_to_dict(record)

        value = record.get(field_name, None)

        # If value is a date or datetime, format it as a string
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        elif isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')

        return value