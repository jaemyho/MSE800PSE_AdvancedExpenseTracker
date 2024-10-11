from sql_statement import *

class CurrencyModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_currencies(self):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(GET_ALL_CURRENCIES)
            self.mysql.connection.commit()
            currencies = cur.fetchall()
            cur.close()
            return currencies
        except Exception as e:
            print(f"Get All Currencies Error : {e}")
            return ()