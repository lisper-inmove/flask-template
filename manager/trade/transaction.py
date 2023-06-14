import proto.trade.transaction_pb2 as transaction_pb
from dao.trade.transaction import TransactionDA
from manager.base_manager import BaseManager
from submodules.utils.idate import IDate


class TransactionManager(BaseManager):

    PAY_METHOD_MAP = {
        "ALIPAY_F2F": "支付宝当面付"
    }

    TYPE_MAP = {
        "CHATBOT_PLUS": "会员"
    }

    STATUS_MAP = {
        "CREATED": "创建",
        "SUCCEED": "成功",
        "REFUNDED": "已退款",
        "CANCELLED": "已取消"
    }

    @property
    def transaction_da(self):
        if not self._transaction_da:
            self._transaction_da = TransactionDA()
        return self._transaction_da

    def _init(self):
        self._transaction_da = None

    def create_transaction(self, req):
        t = self.create_obj(transaction_pb.Transaction)
        t.pay_fee = req.pay_fee
        t.payer_id = req.payer_id
        if req.pay_method != "":
            t.pay_method = transaction_pb.Transaction.PayMethod.Value(req.pay_method)
        if req.type != "":
            t.type = transaction_pb.Transaction.Type.Value(req.type)
        return t

    def get_transaction(self, req):
        transaction = self.transaction_da.get_transaction_by_id(req.transaction_id)
        return transaction

    def list_transactions_by_create_time_periods(self, create_time_periods):
        transactions = self.transaction_da.get_transactions_by_create_time_periods(
            create_time_periods)
        return transactions

    def list_transactions(self, req):
        if req.last_create_time == 0:
            req.last_create_time = IDate.now_timestamp()
        transactions = self.transaction_da.list_transaction(req.last_create_time)
        return transactions

    def list_transaction_by_status(self, req):
        if req.last_create_time == 0:
            req.last_create_time = IDate.now_timestamp()
        transactions = self.transaction_da.list_transaction_by_status(
            req.last_create_time, req.status)
        return transactions

    def count(self):
        return self.transaction_da.count({})

    def count_by_status(self, status):
        return self.transaction_da.count({"status": status})

    def make_transaction_success(self, transaction):
        transaction.status = transaction_pb.Transaction.SUCCEED
        transaction.success_time = IDate.now_timestamp()
        self.add_or_update_transaction(transaction)

    def add_or_update_transaction(self, transaction):
        if not transaction:
            return
        super().update_obj(transaction)
        self.transaction_da.add_or_update_transaction(transaction)
