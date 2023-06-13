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

    def active_list(self):
        recharge_configs = self.recharge_config_manager.get_active_recharge_configs()
        return self.__convert_recharge_config_to_QueryRechargeConfigResponses(
            recharge_configs)

    def list(self):
        recharge_configs = self.recharge_config_manager.list_recharge_configs()
        return self.__convert_recharge_config_to_QueryRechargeConfigResponses(
            recharge_configs)

    def update_status(self):
        req = self.get_request_obj(recharge_config_api_pb.UpdateRechargeConfigStatusRequest)
        recharge_config = self.recharge_config_manager.update_status(req)
        self.recharge_config_manager.add_or_update_recharge_config(recharge_config)
        return self.empty_data_response()

    def __convert_recharge_config_to_QueryRechargeConfigResponse(self, recharge_config):
        r = recharge_config_api_pb.QueryRechargeConfigResponse()
        r.id = recharge_config.id
        r.name = recharge_config.name
        r.level = membership_pb.RechargeConfig.Level.Name(recharge_config.level)
        r.price = recharge_config.price
        r.valid_periods = recharge_config.valid_periods
        r.create_time = recharge_config.create_time_sec
        r.status = membership_pb.RechargeConfig.Status.Name(recharge_config.status)
        return r

    def __convert_recharge_config_to_QueryRechargeConfigResponses(self, recharge_configs):
        result = recharge_config_api_pb.ListRechargeConfigRequest()
        for recharge_config in recharge_configs:
            result.recharge_configs.add().CopyFrom(
                self.__convert_recharge_config_to_QueryRechargeConfigResponse(recharge_config)
            )
        return result
