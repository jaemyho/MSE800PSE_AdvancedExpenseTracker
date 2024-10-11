from models.currency_model import CurrencyModel

class CurrencyController:
    def __init__(self, mysql):
        self.currency_model = CurrencyModel(mysql)

    def get_all_currencies(self):
        return self.currency_model.get_all_currencies()
