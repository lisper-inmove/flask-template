import proto.user.membership_pb2 as membership_pb
from dao.mongodb import MongoDBHelper


class RechargeConfigDA(MongoDBHelper):

    coll = "___user_db___recharge_configs___"

    def add_or_update_recharge_config(self, recharge_config):
        matcher = {"id": recharge_config.id}
        json_data = self.PH.to_json(recharge_config)
        self.update_one(matcher, json_data, upsert=True)

    def get_recharge_config_by_id(self, id):
        matcher = {"id": id}
        recharge_config = self.find_one(matcher, membership_pb.RechargeConfig)
        return recharge_config

    def get_recharge_configs(self):
        recharge_configs = self.find_many({}, enable_empty_matcher=True)
        return self.PH.batch_to_obj(
            recharge_configs, membership_pb.RechargeConfig)
