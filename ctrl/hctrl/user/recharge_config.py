import api.recharge_config_api_pb2 as recharge_config_api_pb
import proto.user.membership_pb2 as membership_pb
from ctrl.base_ctrl import BaseCtrl
from manager.user.recharge_config import RechargeConfigManager


class RechargeConfigCtrl(BaseCtrl):

    @property
    def recharge_config_manager(self):
        if self._recharge_config_manager is None:
            self._recharge_config_manager = RechargeConfigManager()
        return self._recharge_config_manager

    def _init(self, *args, **kargs):
        self._recharge_config_manager = None

    def list(self):
        recharge_configs = self.recharge_config_manager.list_recharge_configs()
        return self.__convert_recharge_config_to_QueryRechargeConfigResponses(
            recharge_configs)

    def __convert_recharge_config_to_QueryRechargeConfigResponse(self, recharge_config):
        r = recharge_config_api_pb.QueryRechargeConfigResponse()
        r.id = recharge_config.id
        r.name = recharge_config.name
        r.level = membership_pb.RechargeConfig.Level.Name(recharge_config.level)
        r.price = recharge_config.price
        r.valid_periods = recharge_config.valid_periods
        return r

    def __convert_recharge_config_to_QueryRechargeConfigResponses(self, recharge_configs):
        result = recharge_config_api_pb.ListRechargeConfigRequest()
        for recharge_config in recharge_configs:
            result.recharge_configs.add().CopyFrom(
                self.__convert_recharge_config_to_QueryRechargeConfigResponse(recharge_config)
            )
        return result
