import proto.user.membership_pb2 as membership_pb

from manager.base_manager import BaseManager
from dao.user.recharge_record import RechargeRecordDA
from submodules.utils.idate import IDate


class RechargeRecordManager(BaseManager):

    @property
    def recharge_record_da(self):
        if self._recharge_record_da is None:
            self._recharge_record_da = RechargeRecordDA()
        return self._recharge_record_da

    def _init(self, *argrs, **kargs):
        self._recharge_record_da = None

    def create_recharge_record(self, req):
        obj = self.create_obj(membership_pb.RechargeRecord)
        return obj

    def list_recharge_records(self, req):
        recharge_records = self.recharge_record_da.get_user_valid_recharge_records(
            req.user_id)
        return recharge_records

    def get_user_latest_paid_recharge_record(self, user):
        return self.recharge_record_da.get_user_latest_paid_recharge_record(user.id)

    def get_recharge_record_by_id(self, id):
        return self.recharge_record_da.get_recharge_record_by_id(id)

    def make_recharge_record_success(self, recharge_record, transaction):
        recharge_record.status = membership_pb.RechargeRecord.PAID
        recharge_record.user_id = transaction.payer_id
        recharge_record.valid_at = recharge_record.config.valid_periods + \
            IDate.now_timestamp()
        self.add_or_update_recharge_record(recharge_record)

    def add_or_update_recharge_record(self, recharge_record):
        if recharge_record is None:
            return
        super().update_obj(recharge_record)
        self.recharge_record_da.add_or_update_recharge_record(recharge_record)
