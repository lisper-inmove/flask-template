import proto.user.membership_pb2 as membership_pb
from dao.mongodb import MongoDBHelper
from submodules.utils.idate import IDate


class RechargeRecordDA(MongoDBHelper):

    coll = "___user_db___recharge_records___"

    def add_or_update_recharge_record(self, recharge_record):
        matcher = {"id": recharge_record.id}
        json_data = self.PH.to_json(recharge_record)
        self.update_one(matcher, json_data, upsert=True)

    def get_recharge_record_by_id(self, id):
        matcher = {"id": id}
        recharge_record = self.find_one(matcher, membership_pb.RechargeRecord)
        return recharge_record

    def get_recharge_records_by_user_id(self, user_id):
        matcher = {"user_id": user_id}
        recharge_records = self.find_many(matcher=matcher)
        return self.PH.batch_to_obj(
            recharge_records, membership_pb.RechargeRecord)

    def get_user_latest_paid_recharge_record(self, user_id):
        matcher = {
            "user_id": user_id,
            "status": "PAID"
        }
        recharge_records = self.find_many(
            matcher=matcher,
            sortby=[("valid_at", -1)],
            page=1,
            size=1,
        )
        for recharge_record in recharge_records:
            return self.PH.to_obj(recharge_record, membership_pb.RechargeRecord)
        return None

    def get_user_valid_recharge_records(self, user_id):
        matcher = {
            "user_id": user_id,
            "valid_at": {"$gt": IDate.now_timestamp()}
        }
        recharge_records = self.find_many(matcher=matcher)
        return self.PH.batch_to_obj(
            recharge_records, membership_pb.RechargeRecord)
