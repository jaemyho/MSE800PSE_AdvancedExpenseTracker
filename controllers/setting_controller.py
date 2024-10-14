from models.setting_model import SettingModel

class SettingController:
    def __init__(self, mysql):
        self.setting_model = SettingModel(mysql)

