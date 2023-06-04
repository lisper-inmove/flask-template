import proto.user.membership_pb2 as membership_pb

from manager.base_manager import BaseManager
from dao.user.recharge_config import RechargeConfigDA


class RechargeConfigManager(BaseManager):

    @property
    def recharge_config_da(self):
        if self._recharge_config_da is None:
            self._recharge_config_da = RechargeConfigDA()
        return self._recharge_config_da

    def _init(self, *argrs, **kargs):
        self._recharge_config_da = None

    def create_recharge_config(self, req):
        obj = self.create_obj(membership_pb.RechargeConfig)
        obj.level = req.level
        obj.valid_periods = req.valid_periods
        obj.price = req.price
        obj.name = req.name
        return obj

    def list_recharge_configs(self):
        recharge_configs = self.recharge_config_da.get_recharge_configs()
        return recharge_configs

    def get_recharge_config_by_id(self, id):
        recharge_config = self.recharge_config_da.get_recharge_config_by_id(id)
        return recharge_config

    def add_or_update_recharge_config(self, recharge_config):
        if recharge_config is None:
            return
        super().update_obj(recharge_config)
        self.recharge_config_da.add_or_update_recharge_config(recharge_config)
