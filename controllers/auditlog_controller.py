from flask import render_template, request, redirect, url_for
from models.auditlog_model import AuditlogModel
from sql_statement import *

class AuditlogController:

    def __init__(self, mysql):
        self.auditlog = AuditlogModel(mysql)

    def view_auditlog(self):
        sql = GET_ALL_AUDITLOG
        type, start_date, end_date = "", "", ""
        if request.method == 'POST':
            type = request.form['search_type']
            start_date = request.form['search_start']
            end_date = request.form['search_end']

            sql = sql[:-1] #removing character ";" at the end
            sql += " WHERE 1=1"

            if type == "weekly":
                sql += " AND YEARWEEK(insert_date) = YEARWEEK(CURRENT_DATE())"
            elif type == "monthly":
                sql += " AND MONTH(insert_date) = MONTH(CURRENT_DATE())"
            elif type == "annually":
                sql += " AND YEAR(insert_date) = YEAR(CURRENT_DATE())"
            if start_date != "":
                sql += " AND insert_date >= '"+start_date+"'"
            if end_date != "":
                sql += " AND insert_date <= '"+end_date+"'"

            sql += ";"

        auditlogs = self.auditlog.get_all_auditlog(sql)
        return render_template('auditlog.html', auditlogs=auditlogs, search_type=type, search_start=start_date, search_end=end_date)