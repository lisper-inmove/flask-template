import proto.config.config_pb2 as config_pb
from manager.base_manager import BaseManager
from dao.config.config import ConfigDA
from view.errors import PopupError


class ConfigManager(BaseManager):

    @property
    def config_da(self):
        if not self._config_da:
            self._config_da = ConfigDA()
        return self._config_da

    def _init(self, *args, **kargs):
        self._config_da = None

    def create_config(self, application_id, name):
        config = self.create_obj(config_pb.Config)
        config.name = name
        config.application_id = application_id
        return config

    def get_config(self, application_id):
        config = self.config_da.get_config_by_application_id(application_id)
        if not config:
            raise PopupError("该应用未配置")
        return config

    def add_or_update_config(self, config, json_data):
        if not config:
            return
        super().update_obj(config)
        self.config_da.add_or_update_config(config, json_data)
