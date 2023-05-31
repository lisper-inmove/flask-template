from flask import request

from ctrl.base_ctrl import BaseCtrl
from manager.config.config import ConfigManager


class ConfigCtrl(BaseCtrl):

    def create(self):
        application_id = request.json.get("application_id")
        name = request.json.get("name")
        config = request.json.get("config")
        manager = ConfigManager()
        obj = manager.create_config(application_id, name)
        manager.add_or_update_config(obj, config)
        return self.empty_data_response()

    def get(self):
        application_id = request.json.get("application_id")
        manager = ConfigManager()
        return manager.get_config(application_id)
